---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: baixa
status: pendente
criado_em: 2026-05-06T21:13:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: implementar
destino_path: api/gpt_inbox.py
contexto: Adicionar leitura recursiva de subpastas no endpoint GET /<secret>/gpt/inbox/<porta>. Hoje o endpoint lê só o nível imediato da pasta.
---

# Leitura recursiva de subpastas no endpoint GPT inbox

## O que fazer

Atualizar `api/gpt_inbox.py` para suportar subpastas dentro dos inboxes.

Hoje o endpoint faz `GET /contents/dialogos/inbox-{porta}/` e processa
so arquivos do nível imediato. Subpastas são ignoradas.

## Implementação sugerida

Substituir `_gh_list()` por `_gh_list_recursive()`:

```python
async def _gh_list_recursive(folder: str) -> list[dict]:
    items = await _gh_list(folder)
    result = []
    for item in items:
        if item["type"] == "file":
            result.append(item)
        elif item["type"] == "dir":
            result.extend(await _gh_list_recursive(item["path"]))
    return result
```

Custo: uma chamada extra à GitHub API por subpasta. Para inboxes com
1-2 subpastas é imperceptível.

## Critério de sucesso

Arquivos `.md` em subpastas de `dialogos/inbox-{porta}/` aparecem
no retorno do endpoint com o path completo.
