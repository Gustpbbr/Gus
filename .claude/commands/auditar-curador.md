Auditar qualidade dos fragmentos do curador no Hub Qdrant.

Argumento opcional: $ARGUMENTS (ex: "haiku", "gpt", "sonnet" — filtra por curador)

**Aviso:** Este comando requer `HUB_READ_TOKEN` configurado no MCP server. Se o token não estiver disponível, o comando retorna erro e indica como proceder.

**Passo 1 — Testar acesso ao Hub**

Chame `mcp__mem0-gus__hub_stats`. Se retornar erro de token, informe:
"Hub inacessível neste ambiente (HUB_READ_TOKEN ausente). Para auditar, rode manualmente via Railway ou GitHub Actions."
E encerre.

**Passo 2 — Buscar fragmentos**

Se $ARGUMENTS especifica um curador (haiku/gpt/sonnet), filtre por esse curador em ambos os brains:
- `mcp__mem0-gus__hub_filtrar(curador=<curador>, user_id="gustavo", limit=200)`
- `mcp__mem0-gus__hub_filtrar(curador=<curador>, user_id="gus", limit=200)`

Se sem argumento, rode também `mcp__mem0-gus__hub_auditar` para visão geral.

**Passo 3 — Análise de qualidade**

Para cada fragmento, avalie:
- **Vago** (conteúdo < 30 chars ou sem substância): 🔴
- **Tipo ausente ou inconsistente**: 🟡
- **Potencial duplicata** (conteúdo similar a outro no lote): 🟡
- **OK**: 🟢

**Passo 4 — Apresentar relatório**

```
=== AUDITORIA CURADOR [<curador ou "todos">] ===

Brain gustavo: <N> fragmentos
Brain gus: <N> fragmentos

🔴 VAGOS (<N>):
  - [<uuid>] "<conteúdo>" — <motivo>

🟡 ATENÇÃO (<N>):
  - [<uuid>] "<conteúdo>" — <motivo>

🟢 OK: <N> fragmentos

AÇÃO SUGERIDA:
  Deletar: <lista de UUIDs vagos> (aguarda confirmação do Gustavo)
  Revisar: <lista de UUIDs com atenção>
```

**Passo 5 — Aguardar instrução**

Nunca deletar automaticamente. Mostre o relatório e pergunte: "Deseja deletar os fragmentos 🔴? Informe quais UUIDs confirmar."
