---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: baixa
status: pendente
criado_em: 2026-05-02T17:35:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: mover
destino_path: ""
contexto: "Apagar arquivo Drive truncado durante upload do protocolo de exames"
---

# Apagar arquivo truncado no Drive

## Contexto

Durante upload do protocolo de exames laboratoriais via Claude Chat (02/05/2026), o método base64 truncou o conteúdo. Foi recriado com sufixo `-completo` usando textContent direto, que funcionou.

Resta apagar o arquivo incompleto.

## Tarefa

Apagar via API Drive o arquivo:
- ID: `1jBqIxa_4jic7upM0vlnKUo1vLj0ArmGx`
- Nome: `protocolo-exames-laboratoriais-v1.md`
- Localização: `Gus-Sync/protocolos/`

O arquivo correto e completo é `protocolo-exames-laboratoriais-v1-completo.md` (ID `1llJJwMNoVfjfHwVgkHjLZYCd2epaIGkZ`) na mesma pasta.

Após apagar, idealmente renomear o `-completo` removendo o sufixo, ficando como `protocolo-exames-laboratoriais-v1.md` — esse é o nome canônico que entra na convenção de versionamento.

-- Claude Chat | via=claude-chat | 02/05/2026
