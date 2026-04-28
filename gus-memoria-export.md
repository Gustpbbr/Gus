---
exportado_em: 2026-04-28T05:01:50
total: 4
fonte: hub-qdrant
---

# Memórias do Gustavo — Export Hub Qdrant

*Última atualização: 28/04/2026 às 05:01*

1. 1. Após merge e deploys recentes, o auto_diagnostico agora tem acesso ao Hub Qdrant (evolução positiva)
2. Problema identificado: Hub Qdrant mostra 0 fragmentos para user_id=gustavo — curador acessível mas vazio ou fragmentos indexados com user_id incorreto
3. Workflow "Ingest Mem0 from Claude Chat" está falhando pós-merge — precisa investigação
4. Gustavo usa estratégia de rodar auto_diagnostico duas vezes em sequência para detectar mudanças pós-deploy
5. Infraestrutura base saudável: GitHub Token (fine-grained PAT), Anthropic Haiku, Tavily search, volume Railway writable funcionando
   *(2026-04-27)*

2. 1. Gustavo quer apagar pendências que estão ultrapassadas — decisão tomada de limpar o backlog desatualizado.
2. Hub contém 204 memórias no total (auditoria de 7:51 BRT).
3. Migração Mem0 → Qdrant ainda não foi concluída; ambos coexistem no momento — o grosso das 204 memórias ainda está no Mem0, apenas ~3 fragmentos indexados no Qdrant com user_id=gustavo.
4. Existem 2 memórias desatualizadas identificadas para deleção: `2b68d542` (sobre workflow falhando) e `cb860bdb` (sobre PR #10 e importações).
5. Workflow de migração para consolidar tudo no Hub Qdrant está disponível e pode ser rodado a critério de Gustavo.
   *(2026-04-27)*

3. 1. Hub Qdrant agora funciona corretamente — 2+ fragmentos salvos, merge resolveu o problema crítico; Gustavo pode enviar PDFs quando quiser.

2. Sistema de curador híbrido (Haiku + Sonnet em paralelo) está operacional com schema gus-18 completo, embeddings locais via sentence-transformers, e controle de ciclo de vida (ativo/histórico/esquecido).

3. Experimento de 14 dias coletando pares Haiku × Sonnet encerra ~12/05/2026; após isso, Gustavo analisará logs em `_log/resumos-mem0/` no Obsidian para decidir qual modelo(s) manter.

4. Canal `dialogos/` operacional em ambas direções: workflow `notificar-inbox-tiogu.yml` notifica bot quando arquivo entra em inbox; tool `rotear_arquivo` permite mover arquivos após confirmação.

5. 16 workflows ativos (dobrou desde última análise): notificação inbox, archive automático, migração Qdrant, migração Mem0→Qdrant, importação Drive, etc.

6. Pendências técnicas: PR #10 ainda aberta (cosmético), workflow "Ingest Mem0 from Claude Chat" falhando (provável endpoint antigo), `memory.py` importa mem0ai à toa (limpeza Fase 5), suporte a vídeo ainda falta.

7. Estrutura repo expandida: novas pastas `api/`, `scripts/`, `_log/`, `agenda/`, `docs/`.
   *(2026-04-27)*

4. 1. Gustavo trabalha com gestão de pacientes organizados por planos de saúde (Assim Taquara vs. outros planos: Intermédica + Leve Saúde)
2. Preferência por separar dados de pacientes em arquivos markdown (.md) segregados por data e tipo de plano
3. Gustavo está testando processamento de PDFs com o Gus — já fez um teste e agora vai testar outro
   *(2026-04-27)*
