---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: media
status: pendente
criado_em: 2026-04-28T19:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: projetos/gus/gus-28-roteamento-multimodelo-tiogu.md
contexto: "Design decision: substituir modelo unico do TioGu por roteamento multi-modelo (GPT-4o-mini para texto, Sonnet para midia), mantendo todos os workflows e tools intactos"
---

# Roteamento Multi-Modelo no TioGu
## Design Decision -- sessao 28/04/2026

Documento gerado em sessao de design entre Gustavo e Claude Chat.
Cobre o problema de custo atual, a arquitetura de roteamento proposta,
o impacto nas capacidades existentes, o que muda no codigo, e a estimativa
de economia.

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

## Decisoes tomadas

1. GPT-4o-mini para mensagens de texto simples
2. Sonnet para qualquer mensagem com midia (foto, documento, video, audio)
3. Haiku para curador -- sem mudanca
4. Nenhum workflow ou tool e alterado
5. Nenhum system prompt e reescrito (apenas ajuste fino opcional)
6. Open source (Gemma/Llama em servidor proprio) em stand-by --
   reavaliar se volume crescer ou se surgir restricao de privacidade

## Resultado
