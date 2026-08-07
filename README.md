# TrilhaSonora — Mini-Projeto

## Como rodar

```powershell
python cli.py
```
Abre o menu interativo. Carrega `catalogo_final.json` automaticamente (caminho
resolvido a partir da pasta do próprio script, não da pasta de onde o comando
é chamado).

```powershell
python main.py
```
Modo batch. Pede o caminho de `consultas.json` e o caminho de saída para
`respostas.json`.

```powershell
python conferir.py
```
Compara `respostas.json` com `gabarito_publico.json` e reporta quantas das
20 consultas públicas bateram.

## Decisões de modelagem

Optei por **não criar classes como `Musica`, `Album` ou `Usuario`**. Cada
conteúdo e cada usuário continuam sendo os dicionários que vêm direto do
JSON, guardados dentro dos índices da `Catalogo`. A razão: nenhuma dessas
estruturas teria comportamento próprio, só campos — tudo que fariam é
guardar dado, e um dicionário já faz isso sem precisar de uma classe em
volta.

A única classe do projeto é a `Catalogo`, e ela se justifica porque agrupa
estado (os índices construídos no `__init__`) com comportamento (os 16
métodos que consultam esse estado) que pertencem juntos: os métodos não
fazem sentido sem os índices, e os índices não servem pra nada sem os
métodos que os consultam.

### Índices construídos no `__init__`

- `id_usuarios` (`{id: usuario}`): acesso direto a um usuário por id, usado
  por `playlist_de`, `conteudo_na_posicao` e `intersecao_playlists`.
- `nome_usuarios` (`{nome.lower(): id}`): resolve nome → id em O(1) e já
  cobre a busca case-insensitive (regra 4) sem precisar normalizar em cada
  chamada.
- `conteudos` (`{id: conteudo}`): acesso direto a um conteúdo por id, usado
  por todos os métodos de "dados de um conteúdo".

**O que não dá pra indexar:** `conteudos_do_genero`. Gênero não é uma chave
fixa no JSON — está espalhado (às vezes string solta, às vezes lista
aninhada em até 3 níveis) e não sabemos os valores possíveis com
antecedência. Um índice `genero -> [ids]` até seria possível construir no
`__init__` achatando tudo uma vez, mas o método atual resolve com uma
varredura em `conteudos_do_genero`, reaproveitando `generos_de` (que já
achata e ordena) para cada item. Funciona porque cada chamada percorre 20
mil itens uma única vez, e as consultas desse tipo não dominam o volume do
`consultas.json`.

### Fila de reprodução

`fila_musicas` usa `collections.deque` em vez de `list`. `enfileirar` só
faz `append` (O(1) no fim); `proximo` faz `popleft` (O(1) no início) — com
`list.pop(0)` isso seria O(n), porque desloca todos os elementos restantes.

### As 7 sujeiras tratadas

| Sujeira | Onde | Tratamento |
|---|---|---|
| `rating` ausente ou como string | `rating_de` | `.get()` + `float()` |
| Álbum sem execuções (`engajamento` ausente) | `execucoes_de` | `.get()` em cascata, retorna `None` |
| Execuções como string com vírgula | `execucoes_de` | `.replace(",", "")` antes de `int()` |
| Data em `DD/MM/YYYY` | `data_adicionado_de` | detecta `"/"`, reordena pra ISO |
| Gêneros como string solta ou lista aninhada | `generos_de` | achatamento com pilha (`_achatar_generos`) |
| Faixa de álbum com `duracao_seg: null` | `duracao_total_de` | soma ignorando `None` |
| Conteúdo sem plataformas | `plataformas_de` | `.get("plataformas", [])` |

Tratamento é pontual (um `.get()` ou `if` por sujeira conhecida), não um
`try/except` genérico envolvendo o método inteiro — cada sujeira tem uma
causa conhecida e um tratamento específico pra ela.

## Verificação

`conferir.py` roda contra as 20 consultas de `gabarito_publico.json` e
reporta acertos, erradas e ausentes separadamente. Resultado atual: **20/20**.