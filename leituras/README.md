# leituras/

Livros e papers lidos / sendo lidos / pra ler.

## Estrutura

- **`livros/`** — `<titulo-curto>.md` por livro. Inclui autor, status
  (lendo/lido/pra-ler), notas, citações, conexões com outros tópicos.
- **`papers/`** — `<titulo-curto>.md` por paper acadêmico. Inclui
  DOI, autores, ano, abstract, anotações, relevância pra projetos.

## Convenções

- Frontmatter: `tipo`, `status` (`lendo`, `lido`, `pra-ler`),
  `relevancia` (1-5), `area`
- Tags via wikilinks pra ligar com projetos: `[[phronesis-bench]]`,
  `[[mge]]`, etc.
- Citações entre aspas com indicação de página

## Diferença

- **`leituras/`**: registro pessoal, anotações, connections.
- **`projetos/<X>/papers/`**: papers específicos de um projeto, ficam
  com o projeto. Aqui em `leituras/papers/` é o pool geral.

## Quando bot salva aqui

Bot detecta links de livros (Amazon, Goodreads, Skoob) ou papers
(arXiv, PubMed) e salva como rascunho aqui pra você completar com
notas depois.
