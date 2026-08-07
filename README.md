# TrilhaSonora

## Rodando o projeto

Pra abrir o menu interativo:
```powershell
python cli.py
```
Ele já carrega o `catalogo_final.json` sozinho, não precisa passar caminho.

Pro modo batch:
```powershell
python main.py
```
Ele pergunta o caminho do `consultas.json` e onde salvar o `respostas.json`.

Pra conferir se as respostas batem com o gabarito público:
```powershell
python conferir.py
```

## Sobre as classes

Só criei uma classe mesmo, a `Catalogo`. Pensei em fazer `Musica`, `Album`,
`Usuario` também, mas não vi motivo — elas não iam fazer nada além de
guardar campo que já vem pronto do JSON. A `Catalogo` é diferente porque
carrega o JSON uma vez, monta uns índices no `__init__`, e os 16 métodos
usam esses índices o tempo todo. Sem os índices os métodos não funcionam,
e os índices sozinhos não servem pra nada — então faz sentido os dois
estarem juntos numa classe.

## Os índices que montei no `__init__`

- `id_usuarios`: dicionário `id -> usuário`, pra achar um usuário na hora
  sem ter que percorrer a lista toda de novo.
- `nome_usuarios`: dicionário `nome em minúsculo -> id`. Já guardo em
  minúsculo pra busca não se importar com maiúscula/minúscula, sem
  precisar tratar isso toda vez que alguém busca.
- `conteudos`: mesma lógica, `id -> conteúdo`.

Gênero eu não consegui indexar direito. Não dá pra saber de antemão quais
gêneros existem, e o campo vem bagunçado — às vezes é string solta, às
vezes lista dentro de lista. Aí o `conteudos_do_genero` varre o catálogo
inteiro mesmo, usando o `generos_de` (que já resolve essa bagunça) pra
cada item. Não é o jeito mais rápido, mas com 20 mil itens ainda dá conta.

## A fila usa deque, não lista

No começo usei lista e funcionava, mas `list.pop(0)` pra tirar o primeiro
da fila é lento — tem que empurrar todo mundo um lugar pra trás. Troquei
pra `collections.deque`, que tira e põe dos dois lados sem esse custo.
Faz mais sentido pra fila, é literalmente pra isso que ela existe.

## As sujeiras dos dados

Essas foram as que encontrei e tratei:

- **Rating ausente ou vindo como string** — confiro se a chave existe
  antes, e converto com `float()`.
- **Álbum sem execuções registradas** — álbum não tem o campo
  `engajamento` que música tem, então uso `.get()` em vez de acessar
  direto e devolvo `None` quando não existe.
- **Execuções com vírgula separando milhar** (tipo `"12,500,000"`) —
  tiro a vírgula antes de converter pra `int`.
- **Data em dois formatos** — a maioria vem `AAAA-MM-DD`, mas tem uns
  casos em `DD/MM/AAAA`. Detecto pela barra e reordeno.
- **Gênero bagunçado** — string solta ou lista aninhada em até uns 3
  níveis. Resolvi com uma função que usa pilha pra achatar tudo numa
  lista só.
- **Faixa de álbum com duração nula** — quando somo a duração das
  faixas, ignoro as que vierem `null`.
- **Conteúdo sem plataforma nenhuma** — devolvo lista vazia em vez de
  quebrar.

Não usei `try/except` genérico em lugar nenhum. Preferi tratar cada
sujeira no ponto exato onde ela aparece — eu sei exatamente quais são
essas 7, então não faz sentido "proteger" o código de coisa que eu já
sei que não vai acontecer.

## Testando

Rodei o `conferir.py` contra o `gabarito_publico.json` e bateu 20/20.
Também testei clonando o repositório numa pasta separada e rodando tudo
de novo do zero, só pra garantir que não ficou nada dependendo de algum
arquivo esquecido na minha pasta de trabalho.