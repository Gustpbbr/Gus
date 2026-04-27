---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-04-27T13:49:00-03:00
processado_em: 2026-04-27T19:55:00-03:00
processado_por: claude-code
---

# OCR com baixa confiança não deve salvar nome — deve pedir reenvio

## Contexto

Gustavo enviou uma foto de OS Dimagem com o texto deitado (rotação 90°). O bot processou a imagem com OCR e registrou um nome **errado** no arquivo `dimagem/dia/2026-04-27.md`, sem nenhum aviso de incerteza. O nome correto era **Gilson Soares de Souza** — e foi registrado como outro paciente.

Isso é erro grave: identidade trocada em contexto médico corrompe toda uma cadeia de ações com consequências reais (procedimento, cobrança, prontuário).

## Ação necessária

Implementar validação de confiança no fluxo de processamento de imagens de OS Dimagem:

1. **Se a confiança do OCR for baixa** (texto ilegível, rotação, qualidade ruim, nome ambíguo) → NÃO salvar. Responder:
   > "Não consegui identificar o nome claramente. Pode reenviar a foto na posição correta?"

2. **Se a confiança for alta** → seguir o fluxo normal (mostrar nome extraído + pedir confirmação).

3. **Nunca registrar um nome com aparência de correto quando há incerteza** — falso positivo nesse contexto é mais perigoso que falso negativo.

## Critério de sucesso

- Foto deitada/ilegível → bot responde pedindo reenvio, sem salvar nada
- Foto clara → fluxo normal de confirmação por nome
- Nenhum nome errado jamais chega ao arquivo `dimagem/dia/`

## Resultado

**Implementado nesta sessão (2026-04-27T19:55).**

### Mudanças

**`gus/dimagem.py`:**

1. `PROMPT_EXTRACAO` ganhou dois campos no schema JSON pedido ao Haiku Vision:
   - `confianca`: "alta" | "media" | "baixa"
   - `motivo_incerteza`: string curta (null se confiança = "alta")
2. Critérios explícitos no prompt:
   - **alta** = imagem nítida, texto reto, NOME lido com 100% de certeza letra por letra
   - **media** = borrão leve OU letras isoladas com leve ambiguidade (contexto resolve)
   - **baixa** = rotação >15°, embaçado/iluminação ruim que torna NOME ambíguo, parte do nome cortada/coberta, **qualquer dúvida sobre quem é o paciente**
3. `analisar_os_dimagem` aplica gate antes de criar pending:
   - `confianca == "baixa"` → retorna `{"pedir_reenvio": True, "preview_text": <pede reenvio>}`. **NÃO** cria state pendente. Loga warning com motivo + nome extraído pra inspeção via `logs_railway`.
   - `confianca == "media"` → preview normal, mas com `⚠️ Confiança média na leitura` e o motivo, alertando o Gustavo a conferir o nome antes de confirmar.
   - `confianca == "alta"` ou ausente/inválida → fluxo normal (default conservador "media" se vier vazio/inválido).

**`gus/bot.py:handle_photo`:**

- Antes de criar `dimagem_pending[chat_id]`, checa `_preview.get("pedir_reenvio")`. Se True, só responde a mensagem de reenvio sem persistir nada — sem chance de "sim" subsequente confirmar nome trocado por engano.

### Critérios atendidos

- ✅ Foto deitada/ilegível → bot responde pedindo reenvio, sem salvar nada (sem state pending)
- ✅ Foto clara → fluxo normal de confirmação por nome (preview limpo)
- ✅ Foto média → preview com aviso visível pedindo dupla checagem (defesa em profundidade)
- ✅ Nenhum nome com confiança baixa chega ao arquivo `dimagem/dia/` — gate é antes do pending, e o pending é o único caminho pro save

### Limitações

- O Haiku auto-avalia confiança via prompt — não tem ground truth. Se ele errar a auto-avaliação ("alta" pra coisa difícil), não bloqueia. Mitigação parcial: o aviso ⚠️ em "media" empurra Gustavo pra checar visualmente no preview antes de confirmar.
- Não detecta nome trocado entre dois pacientes legítimos (ex: Haiku lê "Wilson" quando é "Gilson", ambos parecem nomes válidos). Defesa contra isso continua sendo o passo de confirmação explícita ("sim/não") + leitura atenta do preview pelo Gustavo.
- Validação de logs reais só vai ser possível quando `Railway_diagnostic` for configurado (demanda #5).

### Arquivos tocados

- `gus/dimagem.py` (PROMPT_EXTRACAO + gate em `analisar_os_dimagem`)
- `gus/bot.py` (handler de `pedir_reenvio` em `handle_photo`)
