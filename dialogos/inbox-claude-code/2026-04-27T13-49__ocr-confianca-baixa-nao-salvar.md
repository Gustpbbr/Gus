---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-04-27T13:49:00-03:00
processado_em: ""
processado_por: ""
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
