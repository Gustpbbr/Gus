---
tipo: design-decision
area: gus
gus-id: 29
atualizado: 2026-04-29T12:50-03:00
status: parcial
proximos: Fases 1 e 3 implementadas. Fase 2 (Dimagem em GPT-4o-mini Vision) pendente.
---


# Roteamento Multi-Modelo no TioGu
## Design Decision -- sessao 28/04/2026

Documento gerado em sessao de design entre Gustavo e Claude Chat.
Cobre o problema de custo atual, a arquitetura de roteamento proposta,
o impacto nas capacidades existentes, o que muda no codigo, e a estimativa
de economia.


## Problema

O TioGu hoje usa um unico modelo (provavelmente Sonnet) para todas as
interacoes -- texto simples, fotos, documentos, workflows. Isso e
ineficiente: a maioria das mensagens do Telegram sao texto simples
(perguntas, atualizacoes, comandos) que nao precisam da inteligencia
ou do custo do Sonnet.

Estimativa de uso atual:
- ~80% das mensagens: texto simples (sem midia)
- ~20% das mensagens: foto ou documento anexado

Custo estimado com Sonnet para todo o volume: ~$25-30/mes em tokens.
Custo com roteamento proposto: ~$4-6/mes.
Economia potencial: ~80%.


## Arquitetura de roteamento proposta

O principio central e simples: cada tarefa usa o modelo mais barato
que consegue executa-la bem. O roteamento acontece no bot.py antes
de qualquer chamada de modelo.

FLUXO:

  Mensagem chega no Telegram
          |
  Tem foto, video ou documento anexado?
    SIM -> chama Sonnet (ou GPT-4o Vision)
    NAO -> chama GPT-4o-mini
          |
  Modelo escolhido executa com o mesmo system prompt e tools
          |
  Curador (Haiku) extrai fragmentos -- sem mudanca
          |
  Hub Qdrant recebe fragmentos -- sem mudanca

MODELOS:

  GPT-4o-mini (OpenAI) -- texto simples
    Preco: ~$0.15/1M tokens entrada, $0.60/1M saida
    Capacidades: excelente para seguir instrucoes, responder perguntas,
      acionar tools, processar comandos. Muito bom em portugues.
    Tool calling: suportado nativamente (mesma interface da OpenAI API)
    Latencia: rapido, adequado para bot de Telegram

  Sonnet (Anthropic) -- midia e tarefas complexas
    Preco: $3/1M tokens entrada, $15/1M saida
    Capacidades: visao (fotos de exames, laudos, documentos),
      raciocinio complexo, analise de PDF, OCR avancado
    Quando usar: qualquer mensagem com arquivo anexado,
      perguntas que exijam raciocinio medico complexo

  Haiku (Anthropic) -- curador (sem mudanca)
    Ja em uso no experimento A/B. Correto para extracao de fragmentos.
    Nao muda.


## Impacto nas capacidades existentes

RESPOSTA DIRETA: nenhuma capacidade e perdida. Tudo continua igual.

Os workflows, tools, curador e Hub funcionam independente de qual modelo
responde. Eles nao vivem dentro do modelo -- vivem no codigo do bot.
O modelo recebe o system prompt, decide quais tools chamar, e o bot.py
executa. Isso funciona igual com GPT-4o-mini, Sonnet ou qualquer modelo
que suporte tool calling.

CAPACIDADES QUE CONTINUAM IDENTICAS:

  Disparar workflows n8n -> sem mudanca
    O modelo chama a tool, o bot.py executa o webhook. Independente do modelo.

  Curador extraindo fragmentos -> sem mudanca
    Ja e Haiku. Nao e afetado pelo roteamento.

  Busca e ingestao no Hub Qdrant -> sem mudanca
    Tools de memoria chamadas pelo modelo. Funciona com qualquer modelo.

  Diagnosticos e analise de exames -> MELHORADO
    Antes: Sonnet para tudo (incluindo mensagens simples desperdicando custo)
    Depois: Sonnet especificamente quando ha foto ou documento
    O modelo mais adequado para cada tarefa.

  Respostas a perguntas simples -> mais barato, mesma qualidade
    GPT-4o-mini e suficiente para 'qual meu proximo paciente',
    'anota isso', 'qual o status do projeto X'.

  Registro de informacoes -> sem mudanca
    Tool call para o Hub. Independente do modelo.


## O que muda no codigo

MUDANCAS MINIMAS. O bot.py precisa de tres ajustes:

1. ADICIONAR CLIENT DA OPENAI

   Hoje o bot.py importa apenas o client da Anthropic.
   Adicionar o client da OpenAI ao lado -- duas linhas:

     from anthropic import Anthropic
     from openai import OpenAI

     anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
     openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

2. ADICIONAR FUNCAO DE ROTEAMENTO

   Antes de chamar qualquer modelo, verificar se ha midia na mensagem:

     def tem_midia(update):
         return bool(update.message.photo or
                     update.message.document or
                     update.message.video or
                     update.message.voice)

     def escolher_modelo(update):
         if tem_midia(update):
             return 'sonnet'
         return 'gpt-4o-mini'

3. ADAPTAR A CHAMADA DE MODELO

   Substituir a chamada unica por um if/else que chama o client certo
   baseado no resultado do roteamento. O system prompt, as tools e a
   logica de processamento da resposta permanecem identicos.

   Nota: o formato de tool calling da OpenAI e ligeiramente diferente
   do da Anthropic em alguns detalhes de schema. Claude Code precisa
   adaptar o parser de tool calls para lidar com os dois formatos.
   Nao e complexo -- e um if/else no parser existente.

4. ADICIONAR VARIAVEL DE AMBIENTE

   No Railway: adicionar OPENAI_API_KEY nas variaveis de ambiente.
   Uma linha. Sem mais configuracao.

TOTAL ESTIMADO DE LINHAS ALTERADAS: 30-50 linhas no bot.py
COMPLEXIDADE: baixa
RISCO: baixo -- o fallback natural e o Sonnet se houver duvida


## System prompt: precisa mudar?

O conteudo do system prompt permanece o mesmo.

Ajuste opcional (nao obrigatorio): adicionar uma nota no system prompt
do GPT-4o-mini indicando que ele esta operando como TioGu e deve
seguir as mesmas instrucoes. O GPT-4o-mini segue instrucoes de forma
ligeiramente diferente do Sonnet em alguns detalhes de formatacao e
tom, mas nao o suficiente para exigir reescrita.

Se apos os primeiros dias de uso o comportamento parecer diferente
do esperado em algum aspecto especifico, ajustar o system prompt
pontualmente.


## Capacidades multimodais dos modelos open source (contexto adicional)

Discussao adicional cobriu modelos open source (Gemma, Llama) como
alternativa. Conclusao: nao compensam para o volume atual do TioGu.

GEMMA 3 (Google, open source):
  Versao multimodal disponivel (processa imagens nativamente).
  Para rodar 24/7 com GPU adequada (Gemma 12B): ~$50-80/mes em VPS.
  Para o volume atual do TioGu, GPT-4o-mini via API e mais barato.
  Reconsiderar se volume crescer muito (centenas de usuarios) ou
  se houver restricao de privacidade absoluta (dados nao podem
  sair do servidor proprio).

LLAMA 3.3 70B via Groq:
  Plano gratuito generoso, velocidade muito alta.
  Alternativa viavel ao GPT-4o-mini para texto.
  Nao tem visao nativa na versao 70B.
  Llama 3.2 Vision (11B/90B) tem visao mas qualidade inferior
  ao Sonnet para documentos medicos complexos.

DECISAO: manter Sonnet para midia por qualidade e confiabilidade
em contexto clinico. GPT-4o-mini para texto por custo.
Reavaliar open source quando volume justificar servidor proprio.


## Estimativa de custo

Assumindo 300 mensagens/dia, media de 800 tokens por interacao:

| Cenario                    | Custo/mes estimado |
|----------------------------|--------------------|
| Tudo no Sonnet (atual)     | ~$25-30            |
| 80% GPT-4o-mini, 20% Sonnet| ~$4-6              |
| Economia                   | ~80%               |

Nota: os numeros reais dependem dos logs do Railway.
Claude Code deve verificar o uso atual em tokens antes de implementar
para ter baseline preciso.


## Checklist de implementacao

1. Verificar logs Railway: volume atual de tokens e custo real
2. Adicionar OPENAI_API_KEY nas variaveis de ambiente do Railway
3. Adicionar client OpenAI no bot.py
4. Implementar funcao tem_midia() e escolher_modelo()
5. Adaptar chamada de modelo para usar client correto
6. Adaptar parser de tool calls para lidar com formato OpenAI e Anthropic
7. Testar com mensagem de texto simples -> confirmar GPT-4o-mini
8. Testar com foto -> confirmar Sonnet
9. Testar tool call (workflow, Hub) com GPT-4o-mini -> confirmar funciona
10. Monitorar por 48h e comparar qualidade de respostas
11. Ajustar system prompt do GPT-4o-mini se necessario


## Decisoes tomadas

1. GPT-4o-mini para mensagens de texto simples
2. Sonnet para qualquer mensagem com midia (foto, documento, video, audio)
3. Haiku para curador -- sem mudanca
4. Nenhum workflow ou tool e alterado
5. Nenhum system prompt e reescrito (apenas ajuste fino opcional)
6. Open source (Gemma/Llama em servidor proprio) em stand-by --
   reavaliar se volume crescer ou se surgir restricao de privacidade

## Resultado

---

## Status de implementação (atualizado 2026-04-29)

### Fase 1 — Texto/áudio via GPT-4o-mini ✅ implementado

PR `claude/gus-29-multimodel-fase1`:

- `gus/llm.py`: dispatcher `gerar_resposta()` escolhe provider baseado em content type
- Texto puro → `_gerar_resposta_openai` (gpt-4o-mini, tool calling, prompt caching automático)
- Imagem/document → `_gerar_resposta_anthropic` (Sonnet, prompt caching explícito)
- Áudio → Whisper (já era OpenAI) + texto resultante → gpt-4o-mini
- Adapter: `_anthropic_to_openai_tools()` converte schema das ~21 tools
- Adapter: `_history_to_openai()` converte history bot.py → OpenAI format
- Fallback resiliente: se OpenAI falhar, tenta Anthropic Sonnet automaticamente
- Feature flag `MULTIMODEL_ENABLED` (default true) — rollback de 30s no Railway
- Pricing OpenAI adicionado em `MODEL_PRICING` (gpt-4o-mini, gpt-4o)
- Tracking custo: `cached_tokens` (50% do preço) computado separado

**Diferença vs design original:** o doc fala "Sonnet para mídia". Mantive
Sonnet pra fotos não-Dimagem e PDFs (Fase 1). Dimagem específico é
**Fase 2** (Vision ainda em Anthropic Haiku no `dimagem.py`).

**Economia esperada (Fase 1):** ~80% — texto e áudio são ~80% do volume.

### Fase 2 — Dimagem via GPT-4o-mini Vision ⏳ pendente

Refator `gus/dimagem.py` (ainda usa Haiku Anthropic). Trocar:
- `_e_os_dimagem` (detecção binária) → GPT-4o-mini Vision
- `_extrair_os` (extração JSON) → GPT-4o-mini Vision
- Manter gate de confiança como hoje
- Se confiança baixa → escalar pra Sonnet (fallback de qualidade pra OS difícil)

**Não é blocker pra Fase 1.** Fazer só após Fase 1 estabilizar (1-2 dias).

### Fase 3 — Curador Haiku + GPT-4o-mini ✅ implementado (29/04)

Substitui Sonnet por **GPT-4o-mini** no slot secundário do curador híbrido.

**Motivações:**
1. **Resiliência:** quando crédito Anthropic zera, curador inteiro parava. Agora GPT-4o-mini continua salvando memórias mesmo com Anthropic offline.
2. **Custo:** Sonnet ~$0.001/janela → GPT-4o-mini ~$0.0001/janela (10x menor).
3. **A/B mais informativo:** Haiku × GPT compara famílias diferentes (Anthropic × OpenAI), enquanto Haiku × Sonnet era intra-família.

**Arquivos tocados:**
- `hub/curador.py`:
  - Nova função `_extrair_via_openai()` (paralela a `_extrair_via_modelo()`)
  - `_curar_input_hibrido` substitui `modelo_sonnet` → `modelo_gpt` (env var `MODEL_CURADOR_GPT`, default `gpt-4o-mini`)
  - Salva com `metadata.curador="gpt"` em vez de `"sonnet"`
- `gus/bot.py`: `_resumir_e_salvar` itera `("haiku", ...), ("gpt", ...)` e loga `gpt={N}` em vez de `sonnet={N}`

**Backward compat:**
Fragmentos antigos com `metadata.curador="sonnet"` permanecem inalterados (histórico). Novos fragmentos têm `metadata.curador="gpt"`.

**Trade-off aceito:**
A coleta dual de 14 dias planejada pra ADR-001 Fase 5 (decisão modelo curador final, 12/05) reseta — Haiku × Sonnet só rodou de 27 a 29/04 (3 dias). A nova comparação Haiku × GPT começa em 29/04. Compensação: resiliência prática agora vale mais que continuidade do A/B teórico.

### Fase 4 (futura) — Outras fotos / PDF

Mantém Sonnet por enquanto. Evoluir só se houver caso de uso claro.
