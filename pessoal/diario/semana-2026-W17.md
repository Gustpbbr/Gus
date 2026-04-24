---
tipo: retrospectiva-semanal
semana: 2026-W17
gerado_em: 2026-04-24T20:31:26.256123-03:00
---

# Retrospectiva — semana 2026-W17

## Resumo executivo

A semana foi dominada pela construção da infraestrutura do Gus: saímos de um bot funcional básico para um sistema com persistência, automações, memória ativa e integração Drive→GitHub. Em paralelo, o fluxo do Dimagem ganhou forma concreta com os primeiros arquivos de OS e o padrão `dimagem/dia/` estabelecido. O volume de commits e arquivos criados é alto para uma única semana — o que indica avanço real, mas também alguma desorganização em nomes e duplicatas que vai precisar de curatoria.

---

## Atividades por área

### Projetos — Gus (infraestrutura principal)

Foi a área de maior densidade. Os destaques técnicos em ordem:

- **Persistência**: implementado volume Railway (`/app/data`) via commit `c573cae` — histórico de conversa sobrevive a redeploys.
- **Whisper**: transcrição automática de áudio/voz no Telegram (`8a94b45`) — recurso existia no papel, agora está operacional.
- **SessionStart hook**: Claude Code passa a receber contexto dinâmico em cada sessão (`0b25ab0`).
- **SELF-1 MVP**: reflexão quinzenal automática (Nosis + Thymos + Síntese) rodou pela primeira vez em `2026-04-24 08:01`.
- **Drive Sync**: Apps Script Drive Inbox → GitHub implementado (`bc6fefd`), com OAuth2 resolvendo o problema de quota de service account.
- **search_memory**: bot passou a buscar ativamente no Mem0 (`f69f71b`).
- **Automações**: briefing matinal, retrospectiva semanal, backup Mem0, rate limiting, comando `/custo` — todos implementados em sequência nesta semana.
- **Protocolo `dialogos-tiogu-claude/`**: canal formal inaugurado entre Telegram bot e Claude Code, com [[dialogos-tiogu-claude/semana-2026-04-21.md]] como primeiro registro.
- **Roadmap até Alexa**: consolidado em [[projetos/gus/gus-10-caminho-alexa.md]] com quatro etapas e esforços estimados.
- **Documentação**: série `gus-01` a `gus-10` criada, cobrindo visão, implementado, segurança, portas, autonomia, decisões descartadas, próximos passos, guia de uso e caminho Alexa.

Problemas identificados e corrigidos na semana:
- `_resumir_e_salvar` engolia erros silenciosamente; suspeita de model mal nomeado (`claude-haiku-4-5`).
- `TURNOS_PARA_RESUMO` estava em 5 no Railway, divergindo do system_prompt que dizia 3 — corrigido em `55ebd11`.
- Bot alucinava "arquivo não existe" sem verificar — regra adicionada ao system_prompt (`7738295`).
- Gus confirmava ações sem executar — regra operacional reforçada.

### Dimagem

Primeiro dia de uso sistemático do fluxo estruturado foi **24/04/2026** (sábado), com 6 pacientes em São Gonçalo e Nova Iguaçu.

- Padrão de pasta estabelecido: `dimagem/dia/AAAA-MM-DD.md`, um arquivo por dia, append por foto.
- Arquivo do dia criado: [[dimagem/dia/2026-04-24.md]] e retroativo [[dimagem/dia/2026-04-20.md]].
- Regra de privacidade documentada: nomes de paciente permitidos no repositório; CPF/RG vão para `sensivel/`.
- Pacientes do dia com anotações clínicas relevantes: fasting, contraste não autorizado, peso para dose, status internado/ambulatorial.
- Problema de fragmentação: 5 arquivos com conteúdo idêntico espalhados em `casos/`, `ordens-servico/` e `fechamento/` — resolvido com limpeza, mantendo apenas [[dimagem/fechamento/os-24042026.md]].
- Próximo passo registrado como pendência: deletar `dimagem/casos/` e `dimagem/ordens-servico/` via `dialogos-tiogu-claude/`.

### Capturado

- Agenda de abril a dezembro 2026 criada em `agenda/` — 8 arquivos mensais com compromissos diários em formato simples. Duplicação identificada (6 commits, 3 arquivos duplicados) e resolvida.
- Lista dos 100 melhores filmes do século XXI (NYT) iniciada — dados extraídos de fotos de filmes enviadas; Gus travou na execução mas o registro foi retomado.
- Receitas salvas: [[receitas/salgadas/feijoada-cha-de-cravo.md]] (com técnica do chá de cravo e base científica dos ingredientes) e [[receitas/doces/romeu-e-julieta-cremoso.md]].
- Falso positivo no scan de dados sensíveis: palavra "cravo" acionou redirecionamento para `sensivel/` — comportamento registrado para ajuste futuro.

### Saúde

Atividade leve. Nenhum arquivo de saúde criado esta semana além dos índices. O [[_indices/saude.md]] foi gerado, mas `historico-saude.md` — solicitado em 23/04 — ainda não foi criado. Único registro clínico pessoal: envolvimento com procedimentos de RM com anestesia em 24/04 (Hidro-RM, RM abdominal superior, RM pélvica).

### Outras

- **Jardim/plantas**: diagnóstico detalhado de pragas em 23/04 — pulgão em cítricos, cochonilha e antracnose em orquídeas (Cattleya). Plano de manejo integrado definido com produtos específicos.
- **Índices MOC**: estrutura completa criada em `_indices/` — 8 categorias (master, capturas, clínica, financeiro, projetos, receitas, saúde, auditoria Mem0).
- **Memória Gus**: sistema com 2 cérebros no Mem0 (`user_id gus` separado de `gustavo`) implementado (`18c73a5`).
- **Phronesis-Bench**: pasta criada no repositório, prazo de 16/04 expirado, sem arquivos, status desconhecido.

---

## Decisões tomadas

| Decisão | Justificativa |
|---|---|
| Um arquivo por dia em `dimagem/dia/` com append por foto | Elimina fragmentação e facilita fechamento do dia com o comando `fecha o dia` |
| Nomes de paciente permitidos no repo; só CPF/RG vão para `sensivel/` | Equilíbrio entre praticidade clínica e proteção de dados |
| Drive Sync via OAuth2 (em vez de service account) | Cota de service account causava falhas; OAuth2 resolveu |
| Gus é a entidade, bot é a porta (ontologia explícita) | Clareza arquitetural para evitar confusão de identidade nas próximas expansões |
| `TURNOS_PARA_RESUMO` = 3 (revertido de 5) | Consistência entre Railway e system_prompt |
| Tarefas com datas e conteúdo preciso: Claude Sonnet, não Haiku | Qualidade de extração justifica custo maior |
| `dialogos-tiogu-claude/` como canal formal de delegação entre Telegram e Claude Code | Rastreabilidade de dem
