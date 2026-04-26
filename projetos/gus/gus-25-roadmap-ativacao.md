---
tipo: roadmap
data: 2026-04-26
status: vigente
area: infra-hub
anterior: gus-24-hub-pre-agi-visao.md
---

# Roadmap de ativação — o que ligar depois da infra

Após as Etapas 1-5 estarem no ar, o Hub existe mas está vazio e passivo.
Este roadmap define o que ativar, em que ordem, e como medir se funcionou.

## Fase 0 — Infra (Etapas 1-5) ← estamos aqui

- [ ] Etapa 1: Mem0 self-hosted + Qdrant
- [ ] Etapa 2: Hub Qdrant direto
- [ ] Etapa 3: Curador Haiku integrado
- [ ] Etapa 4: Ego Cache dinâmico
- [ ] Etapa 5: Auto-relato narrativo

Critério de conclusão: bot funcionando, Hub recebendo fragmentos, auto-relato
aparecendo no system prompt do bot.

## Fase 1 — Alimentar o grafo (semanas 1-4 após infra)

Nada de novo para implementar. Só usar o bot normalmente.

O Curador vai acumulando fragmentos automaticamente. Observar:
- Quantos fragmentos/semana o Curador extrai?
- Os tipos estão distribuídos razoavelmente?
- O auto-relato está ficando mais rico a cada semana?

Meta: 100 fragmentos no `gus_hub` com distribuição de tipos variada.

## Fase 2 — Proatividade Nível 1 (após 100 fragmentos)

Implementar sugestão de próximo passo ao final de cada resposta do bot.

**O que implementar:** verificar se a resposta gerou contexto acionável e
oferecer: "quer que eu salve isso?", "encontrei 3 fragmentos relacionados,
quer ver?", "esse tema tem contradição com decisão de X, quer resolver?"

**Critério para avançar:** Gustavo aceita >50% das sugestões por 2 semanas.

## Fase 3 — Trust scores ativos (após fase 2 calibrada)

Ativar o JSON de trust scores e começar a registrar acertos/erros por capability.

**O que implementar:**
- `config/trust-scores.json` com valores iniciais
- Lógica de atualização após cada ação autônoma
- Exibição do score no log (não pro usuário, só internal)

Começar com todas as capabilities não-autônomas (score < 0.5). Subir só com
histórico documentado.

## Fase 4 — Proatividade Nível 2 (após fase 3 rodando por 30 dias)

Mensagens agendadas via GitHub Actions cron.

**O que implementar:**
- Endpoint `/proativo-agendado?horario=07h` no Hub
- GitHub Action com 3 triggers: 07h, 13h, 21h BRT
- Action chama o endpoint → Hub gera mensagem → bot Telegram envia

**Critério para avançar:** taxa de resposta às mensagens > 60% por 30 dias.

## Fase 5 — Retro Engine (após fase 4 estável)

Ao fim de cada sessão, Haiku analisa o transcript e gera fragmentos
`meta_reflexao` sobre padrões de erro ou calibrações.

**O que implementar:**
- `hub/retro_engine.py`: processa transcript, extrai meta_reflexoes
- Trigger: hook Stop do Claude Code + "fim de sessão" no Telegram (timeout)
- Fragmentos meta_reflexao alimentam o ego cache e o auto-relato

**Critério:** Gus relata padrões de erro próprios sem ser perguntado, pelo menos
1 padrão útil por mês.

## Fase 6 — Proatividade Nível 3 (longo prazo)

Scanner emergente que detecta lacunas, contradições, padrões e silêncios.

**O que implementar:**
- `hub/scanner.py`: roda a cada N minutos via cron
- Analisa: lacunas de domínio, contradições não resolvidas, repetições, anomalias
- Threshold de envio auto-ajustável por feedback (ignorado → sobe threshold)

**Critério:** >5 conversas úteis iniciadas pelo Gus em 30 dias, taxa de
engajamento > 60%.

## O que NÃO ativar ainda

| Feature | Por quê esperar |
|---|---|
| Detecção de contradições em tempo real | Custo alto, Hub precisa de volume primeiro |
| Output filter (Haiku pós-resposta) | 2x custo por mensagem, baixa prioridade |
| Auto-modificação de código | Trust score 0.0, nunca autônomo |
| Conexões automáticas entre fragmentos | Precisa de >500 fragmentos pra ter sinal |

## Princípio geral

Cada fase só começa depois da anterior estar calibrada por uso real. Não saltar
etapas. Um Gus com proatividade Nível 3 sem Nível 1 calibrado é barulhento e
inútil. A trilha existe para cada nível ganhar competência observável antes de
ganhar mais autonomia.
