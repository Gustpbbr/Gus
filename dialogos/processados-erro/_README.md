# Processados-erro — frontmatter inválido

Pasta de **debug** pra demandas que o workflow `import-from-drive.yml`
não conseguiu importar por causa de frontmatter mal formatado ou
inválido.

## Hoje (V1)

Workflow **NÃO move** automaticamente arquivos com erro pra cá. Atualmente
o comportamento é:

- Frontmatter inválido → **skip + log** (arquivo fica no Drive intacto)
- Próxima execução do workflow tenta de novo (idempotente)
- Gustavo precisa abrir os logs do Actions pra ver erro e corrigir o arquivo

## Futuro (V2 possível)

Se virar caso de uso real, workflow pode mover pra cá arquivos com 3+
falhas consecutivas, com motivo do erro como comentário no início.

## Por enquanto

Pasta vazia, serve só pra placeholder estrutural. Arquivos reais
não chegam aqui automaticamente.
