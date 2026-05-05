---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: media
status: pendente
criado_em: 2026-05-02T22:30:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: ""
contexto: "Registrar existência do Protocolo de Análise de Exames v1 + 2 JSONs estruturados em pessoal/saude/, e ingerir cada exame como fragmento rastreável no Hub Qdrant"
---

# Ingestão de exames laboratoriais como fragmentos no Hub Qdrant

## Contexto

Nesta sessão de Claude Chat (02/05/2026) construímos um sistema completo de análise estruturada de exames laboratoriais. Os artefatos produzidos:

1. **Protocolo de Análise IA de Exames Laboratoriais v1** — em `Gus-Sync/protocolos/protocolo-exames-laboratoriais-v1.md`. Define 8 fases sequenciais que qualquer IA executa sobre um exame, gerando saída estruturada reproduzível.

2. **2 JSONs estruturados (paciente_id=gus)** em `Gus-Sync/pessoal/saude/`:
   - `gus__2026-01-27__lafe.json` — exames LAFE de jan/2026 (Doença de Graves ativa, dislipidemia, hiperinsulinemia)
   - `gus__2019-11-18__lafe.json` — exames LAFE de nov/2019 (linha de base pré-Graves, dislipidemia já presente)

3. **2 MDs narrativos** correspondentes (análises interpretativas).

4. **HTML reader** (`reader-exames-v0.2.html`, em desenvolvimento) que carrega múltiplos JSONs e renderiza visualização longitudinal.

## O que precisa ser feito

### Parte 1 — Registro estrutural

Criar awareness no Mem0 (brain `gustavo`, tag `via=claude-chat`) sobre a existência:
- Do protocolo em `protocolos/protocolo-exames-laboratoriais-v1.md`
- Dos JSONs estruturados em `pessoal/saude/gus__*__*.json`
- Da convenção de nomenclatura `<paciente_id>__<data_coleta>__<lab_curto>.json`
- Do `paciente_id` canônico `gus` (lowercase, sem acentos)

### Parte 2 — Ingestão de fragmentos rastreáveis

**Cada valor de exame deve virar um fragmento rastreável no Hub Qdrant**, conforme schema unificado abaixo. Backfill retroativo nos 2 JSONs já existentes, e pipeline contínuo para novos JSONs depositados em `pessoal/saude/`.

## Schema único de fragmento

Todo fragmento usa o mesmo schema. Campos não-aplicáveis ao tipo ficam `null`.

```json
{
  "id": "string (determinístico: frag_<paciente_id>_<data_coleta>_<chave>)",
  "tipo_fragmento": "exame_pontual | analise_painel | achado_clinico",
  "texto_para_embedding": "string (auto-contido, narrativo, com contexto clínico mínimo)",

  "metadata": {
    "paciente_id": "string",
    "data_coleta": "YYYY-MM-DD",
    "idade_na_coleta": "number",
    "sexo": "M | F | outro",
    "laboratorio": "string",
    "contexto_clinico": "string",
    "data_analise": "YYYY-MM-DD",
    "modelo_ia": "string",
    "protocolo_versao": "string",
    "fonte_arquivo": "string",
    "criado_em": "ISO 8601 -03:00",

    "exame": "string ou null",
    "exame_label": "string ou null",
    "valor": "number | string | null",
    "valor_numerico": "number ou null",
    "unidade": "string ou null",
    "ref_min": "number ou null",
    "ref_max": "number ou null",
    "ref_texto": "string ou null",
    "fonte_ref": "string ou null",
    "status": "string ou null",
    "metodo": "string ou null",
    "painel": "string ou null",
    "painel_secundario": "string ou null",

    "alteracoes": "array<string> ou null",
    "exames_normais_no_painel": "array<string> ou null",
    "conclusao_curta": "string ou null",

    "categoria": "string ou null",
    "achado_curto": "string ou null",
    "paineis_envolvidos": "array<string> ou null",
    "exames_chave": "array<string> ou null",
    "probabilidade": "alta | media | baixa | null",
    "acao_sugerida": "string ou null"
  }
}
```

### Regras de preenchimento por tipo

**`exame_pontual`** — preenche bloco "exame_*" e `painel`. Nulls nos blocos "alteracoes_*" e "categoria_*".

**`analise_painel`** — preenche `painel`, `alteracoes`, `exames_normais_no_painel`, `conclusao_curta`. Nulls no bloco "exame_*" e "categoria_*".

**`achado_clinico`** — preenche `categoria`, `achado_curto`, `paineis_envolvidos`, `exames_chave`, `probabilidade`, `acao_sugerida`. Nulls no bloco "exame_*" e "alteracoes_*".

## Convenção de IDs (determinísticos)

- `exame_pontual`: `frag_<paciente_id>_<data_coleta>_<exame>` → `frag_gus_2026-01-27_ldl`
- `analise_painel`: `frag_<paciente_id>_<data_coleta>_painel_<painel>` → `frag_gus_2026-01-27_painel_lipidico`
- `achado_clinico`: `frag_<paciente_id>_<data_coleta>_achado_<categoria>` → `frag_gus_2026-01-27_achado_hipogonadismo_compensado`

**Substituição:** se um fragmento com mesmo ID já existe, a re-ingestão **substitui** (não cria duplicata). Permite re-rodar o protocolo v2 no futuro sem poluir.

## Quantidade esperada de fragmentos

- **JSON de 2026-01-27** (~38 exames, 6 painéis com alterações, 3 achados clínicos): ~47 fragmentos
- **JSON de 2019-11-18** (~25 exames, 3 painéis com alterações, 1 achado): ~30 fragmentos
- **Total backfill inicial:** ~77 fragmentos

## Regras de geração

### Para `exame_pontual`
- **Gerar para TODOS os exames** (mesmo normais), pois futuros podem virar alterados e a busca histórica precisa do dado.
- `texto_para_embedding` deve incluir: data, idade, paciente, valor, unidade, status, referência, painel, contexto clínico curto, método (se relevante).
- Exemplo: *"Em 27/01/2026, Gustavo (41 anos, masculino) tinha LDL-colesterol 172 mg/dL, status alto (referência: <130 mg/dL para baixo risco cardiovascular pela diretriz SBC 2017). Painel: lipídico. Coleta no laboratório LAFE em contexto de Doença de Graves em uso de tapazol, sedentário. Método: cálculo Martin/Hopkins."*

### Para `analise_painel`
- **Gerar apenas se o painel tem pelo menos 1 alteração.**
- Sumariza o painel: lista alterações, lista normais, conclusão curta.
- Cruza com a análise narrativa do MD correspondente para extrair conclusão clínica.

### Para `achado_clinico`
- **Gerar a partir do array `discordancias_internas` + `hipoteses` do JSON.**
- Cada hipótese de probabilidade `alta` ou `media` vira um fragmento.
- `categoria` em snake_case_pt_br (ex: `hipogonadismo_compensado`, `dislipidemia_mista`, `resistencia_insulinica`).
- `texto_para_embedding` é narrativo e auto-contido — quem ler entende o achado sem precisar do JSON inteiro.

## Política de saúde (registrar no Mem0)

Os dados de saúde do Gustavo:
- **Pasta canônica:** `Gus-Sync/pessoal/saude/` no Drive
- **Sem propagação automática para GitHub público** (a pasta `pessoal/saude/` não é sincronizada bidirecionalmente — só Drive)
- **Pode virar fragmento no Hub Qdrant** (decisão do usuário em 02/05/2026)
- **Schema dos fragmentos:** documentado nesta demanda
- **Convenção de nomenclatura:** `<paciente_id>__<data_coleta>__<lab_curto>.json`

## Critério de sucesso

1. Mem0 do brain `gustavo` tem memória registrando existência do protocolo + JSONs + convenção de nomenclatura.
2. Hub Qdrant tem ~77 fragmentos com schema correto após backfill dos 2 JSONs existentes.
3. Pipeline contínuo configurado: novos JSONs em `pessoal/saude/` geram fragmentos automaticamente.
4. Buscas semânticas no Hub do tipo "como tá meu LDL?", "qual minha testo em 2019?", "tenho hipogonadismo?" retornam fragmentos relevantes.
5. Notificação Telegram quando o backfill concluir.

## Observações para execução

- Se algum campo do JSON original estiver faltando ou inconsistente, **logar erro** e não criar o fragmento (não inventar dados).
- A `categoria` dos `achado_clinico` deve seguir a convenção `snake_case_pt_br` — se uma nova categoria aparecer, registrar em log para canonização posterior.
- O pipeline contínuo deve detectar novos JSONs em `pessoal/saude/` (watcher ou cron) e ingerir automaticamente.
- **Não substituir** o JSON original ao gerar fragmentos — JSON é a fonte da verdade, fragmentos são derivados.

## Arquivos relacionados

- `Gus-Sync/protocolos/protocolo-exames-laboratoriais-v1.md` — protocolo completo com schema dos JSONs
- `Gus-Sync/pessoal/saude/gus__2026-01-27__lafe.json`
- `Gus-Sync/pessoal/saude/gus__2026-01-27__lafe__analise.md`
- `Gus-Sync/pessoal/saude/gus__2019-11-18__lafe.json`
- `Gus-Sync/pessoal/saude/gus__2019-11-18__lafe__analise.md`

---

-- Claude Chat | via=claude-chat | 02/05/2026
