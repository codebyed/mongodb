# PyODMongo

**PyODMongo** é uma biblioteca moderna em Python que atua como um Mapeador Objeto-Documento (ODM) para **MongoDB**. Construída sobre o **Pydantic V2**, ela faz uma ponte perfeita entre Python e MongoDB, oferecendo uma maneira intuitiva e eficiente de interagir com documentos. ([doc oficial pt-BR, linha 21](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L21))

Como a classe `DbModel` é uma extensão de `BaseModel` do Pydantic, todos os recursos do Pydantic (Validators, Fields, Model Config) ficam disponíveis nos modelos. ([doc oficial, linha 23](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L23))

- **Documentação oficial**: https://pyodmongo.dev
- **Repositório**: https://github.com/mauro-andre/pyodmongo
- **PyPI**: https://pypi.org/project/pyodmongo
- **Licença**: MIT ([doc oficial, linha 50](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L50))

## Principais recursos

| Recurso | Descrição | Referência |
|---|---|---|
| **Integração com Pydantic** | Validação de dados e modelagem do Pydantic ao trabalhar com dados do MongoDB. | [doc oficial, linha 27](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L27) |
| **Geração automática de esquema** | Defina o esquema com modelos Pydantic e as coleções são criadas automaticamente. | [doc oficial, linha 29](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L29) |
| **Construtor de queries** | Construa consultas complexas do MongoDB usando código Python puro. | [doc oficial, linha 31](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L31) |
| **Serialização de documentos** | Serializa e desserializa objetos Python para documentos MongoDB. | [doc oficial, linha 33](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L33) |
| **Suporte assíncrono** | API `async` (`AsyncDbEngine`) e síncrona (`DbEngine`). | [doc oficial, linha 35](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L35) |
| **Desenvolvimento ativo** | Projeto mantido regularmente com novas funcionalidades. | [doc oficial, linha 37](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L37) |

> Todas as seis características acima estão listadas na página "Visão geral" da documentação oficial, sob "Principais Recursos" ([index.md L25-L37](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L25)).

## Requisitos

- Python 3.11+ ([badge oficial](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L11))
- MongoDB
- Pydantic V2

## Instalação

```bash
pip install pyodmongo
```

Fonte: [doc oficial, linhas 39-45](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L39).

## Primeiros passos

### 1. Criando o motor

Crie uma instância de `AsyncDbEngine` (assíncrono) ou `DbEngine` (síncrono) para conectar ao MongoDB ([doc oficial, linha 7](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/getting_started.md#L7)):

```python
from pyodmongo import AsyncDbEngine, DbModel
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')
```

```python
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')
```

> **Dica**: Ao criar o motor, é possível passar o parâmetro `tz_info`, que define o fuso horário padrão para todas as operações de `find_one` e `find_many` daquele motor. Se `tz_info` também for passado nos métodos de busca, o fuso horário dos métodos tem prevalência. ([doc oficial, linha 24](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/getting_started.md#L24))

### 2. Definindo um modelo

Crie uma classe que herda de `DbModel` e defina o atributo `_collection` (um `ClassVar` com o nome da coleção / estrutura dos documentos) ([doc oficial, linha 27](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/getting_started.md#L27)):

```python
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'
```

### 3. Salvando dados

Você pode salvar dados no MongoDB usando o método `save()` da sua instância `AsyncDbEngine` ou `DbEngine` ([doc oficial, linha 44](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/getting_started.md#L44)):

```python
box = Product(name='Box', price=5.99, is_available=True)
result = await engine.save(box)  # async
# result = engine.save(box)      # sync

async def main():
    result = await engine.save(box)

asyncio.run(main())
```

Se o `save` resultar na criação de um novo documento, a instância recebe automaticamente os atributos `id`, `created_at` e `updated_at`. ([doc oficial, linha 23 da pág. Save](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L23))

### 4. Lendo do banco

Para ler dados do banco de dados, você pode usar o método `find_one()` da sua instância `AsyncDbEngine` ou `DbEngine` ([doc oficial, linha 61](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/getting_started.md#L61)):

```python
product = await engine.find_one(Product, Product.name == 'Box')
# product = engine.find_one(Product, Product.name == 'Box')  # sync
```

## DbModel

Cada classe que herda de `DbModel` representa automaticamente uma coleção no MongoDB ([doc oficial, linha 3](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L3)). O atributo `_collection` é obrigatório para mapear a classe para a coleção correspondente, sendo um `ClassVar` com o nome desejado ([doc oficial, linha 11](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L11)).

### Atributos herdados

| Atributo | Tipo | Descrição | Referência |
|---|---|---|---|
| `id` | `Id` | Identificador exclusivo do documento. Gerado automaticamente se não informado. Corresponde ao `_id` do MongoDB e é armazenado como `ObjectId`. | [doc oficial, L17](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L17) |
| `created_at` | `datetime` | Carimbo de data/hora de criação do documento. Gerido pela biblioteca e gerado automaticamente. | [doc oficial, L29](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L29) |
| `updated_at` | `datetime` | Carimbo de data/hora da última modificação. Atualizado automaticamente. | [doc oficial, L33](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L33) |

> O `Id` é processado pelo PyODMongo para ser armazenado como `ObjectId`. Você pode inserir um `str` ou `ObjectId` que a conversão é feita de forma transparente. ([doc oficial, linha 22](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L22))

### Relacionamentos

Relacionamentos em PyODMongo são modelados por referências ou documentos incorporados ([doc oficial, linha 37](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L37)).

#### Por referência

Relacionamentos por referência envolvem referenciar um documento a outro usando um identificador ([doc oficial, linha 41](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L41)). O PyODMongo aceita que o campo seja uma instância do modelo ou uma referência `Id` ([doc oficial, linha 47](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L47)):

```python
class Post(DbModel):
    title: str
    user: User       # instância de User ou Id
    _collection: ClassVar = 'posts'
```

Também é possível usar listas de referências: `user: list[User | Id]`. ([doc oficial, linha 50](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L50))

#### Documentos incorporados

Documentos incorporados envolvem aninhar um documento dentro de outro ([doc oficial, linha 54](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L54)), usando `MainBaseModel` (ou `BaseModel` do Pydantic):

```python
from pyodmongo import MainBaseModel

class Address(MainBaseModel):
    street: str
    city: str

class User(DbModel):
    name: str
    address: Address
    _collection: ClassVar = 'users'
```

> **Nota**: `MainBaseModel` é recomendado pois alguns operadores de busca, como `$elemMatch`, exigem `MainBaseModel` para elementos aninhados. Também é possível incorporar outros objetos `DbModel`. ([doc oficial, linhas 66-71](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md#L66))

## Operações CRUD com DbEngine / AsyncDbEngine

### save

O método `save` faz parte das classes `AsyncDbEngine` e `DbEngine`. É responsável por salvar ou atualizar documentos no banco de dados ([doc oficial, linha 5](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L5)).

- `obj: Any` — Objeto a ser salvo no banco de dados. [L27](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L27)
- `query: ComparisonOperator | LogicalOperator = None` — Consulta para atualizar documentos. Se não informada e `obj` tem `id`, atualiza o documento com aquele `_id`; se `obj` não tem `id`, cria um novo documento. [L28](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L28)
- `raw_query: dict = None` — Consulta no formato nativo do MongoDB. [L29](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L29)
- `upsert: bool = True` — Insere o documento se nenhum correspondente for encontrado. [L30](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L30)

> **Aviso**: Se `query` for passado, `raw_query` é ignorado ([L33](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L33)).
> Por baixo dos panos, usa `update_many` com `upsert=True` ([L36](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L36)).

Também existe o método `save_all`, que salva uma lista de objetos ([doc oficial, linha 40](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L40)).

### save_all

```python
products = [Product(name='Box', price=5.99, is_available=True),
            Product(name='Ball', price=7.50, is_available=True)]
await engine.save_all(products)  # async
# engine.save_all(products)      # sync
```

O retorno de `save_all` é um dicionário cujas chaves são os nomes das coleções e os valores são objetos `DbResponse`. ([doc oficial, linha 61](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L61))

### find_one

O método `find_one` é usado para recuperar um único objeto do banco de dados com base em critérios especificados ([doc oficial, linha 5](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L5)).

- `Model: DbModel` — Classe modelo a ser instanciada. [L20](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L20)
- `query` — Consulta para filtrar. [L21](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L21)
- `raw_query: dict` — Consulta nativa MongoDB. [L22](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L22)
- `sort: SortOperator` — Lista de tuplas `(campo, direção)` com `1` (ascendente) ou `-1` (descendente). [L23](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L23)
- `raw_sort: dict` — Classificação em formato nativo MongoDB. [L24](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L24)
- `populate: bool` — Se `True`, preenche os campos de relacionamento com outros objetos. [L25](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L25)
- `as_dict: bool` — Retorna a resposta como dicionário (útil para JSON em APIs). [L26](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L26)
- `tz_info: timezone` — Fuso horário para campos `datetime`. [L27](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L27)

> Se `query` for passado, `raw_query` não será considerado ([L30](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L30)).

### find_many

O método `find_many` é semelhante ao `find_one`, mas recupera uma lista de objetos que correspondem aos critérios especificados ([doc oficial, linha 34](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L34)). Inclui três argumentos extras para paginação:

- `paginate: bool` — Se `True`, encapsula a resposta em `ResponsePaginate`. [L51](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L51)
- `current_page: int` — Página atual. [L52](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L52)
- `docs_per_page: int` — Máximo de documentos por página. [L53](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L53)

### Paginação

Quando `paginate=True`, o resultado é encapsulado em um objeto `ResponsePaginate` ([doc oficial, linha 57](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L57)):

```python
result = await engine.find_many(
    Product,
    Product.name == 'Box',
    paginate=True,
    current_page=1,
    docs_per_page=10
)
```

O objeto `ResponsePaginate` contém ([L59-L62](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L59)):

- `current_page: int` — Indica a página atual. [L59](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L59)
- `page_quantity: int` — Total de páginas. [L60](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L60)
- `docs_quantity: int` — Total de documentos encontrados. [L61](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L61)
- `docs: list[Any]` — Documentos da página atual. [L62](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L62)

### populate

O recurso populate preenche automaticamente todas as referências dentro de um objeto, incluindo referências aninhadas ([doc oficial, linha 79](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L79)):

- Quando `populate=True` em `find_one` ou `find_many`, todas as referências são preenchidas. [L81](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L81)
- Referências com referências adicionais também são preenchidas recursivamente. [L82](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L82)
- Listas de referências também são populadas. [L83](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L83)

Para bom desempenho, o PyODMongo aproveita a estrutura de agregação do MongoDB por baixo dos panos. ([nota oficial, L86](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md#L86))

### delete

O método `delete` exclui documentos de uma coleção MongoDB com base em uma consulta especificada ([doc oficial, linha 5](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L5)).

- `Model: DbModel` — Modelo base para a consulta. [L20](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L20)
- `query` — Critérios de seleção. [L21](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L21)
- `raw_query: dict (opcional)` — Consulta nativa. [L22](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L22)

> **Aviso**: O `delete` usa `delete_many` internamente — todos os documentos que corresponderem à consulta serão excluídos. ([doc oficial, linha 25](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L25))

### delete_one

Semelhante ao `delete`, mas exclui apenas o primeiro documento que corresponder à consulta. ([doc oficial, linha 30](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L30))

### DbResponse

As operações de `save` e `delete` retornam um objeto `DbResponse` ([doc oficial, L44 da pág. Delete](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md#L44) e [L65 da pág. Save](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L65)):

| Atributo | Tipo | Descrição | Referência |
|---|---|---|---|
| `acknowledged` | `bool` | Se a operação foi reconhecida pelo servidor. | [L65](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L65) |
| `deleted_count` | `int` | Número de documentos excluídos. | [L67](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L67) |
| `inserted_count` | `int` | Número de documentos inseridos. | [L69](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L69) |
| `matched_count` | `int` | Documentos que corresponderam à consulta. | [L71](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L71) |
| `modified_count` | `int` | Documentos efetivamente modificados. | [L73](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L73) |
| `upserted_count` | `int` | Documentos inseridos via upsert. | [L75](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L75) |
| `upserted_ids` | `dict[int, Id]` | Índice dos documentos inseridos mapeado para seus novos IDs. | [L77](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md#L77) |

## Operadores de query

As consultas são construídas de forma pythônica, com operadores mágicos ou com a API `eq`, `gt`, etc. do PyODMongo. As consultas são atributo essencial dos métodos `find_many`, `find_one`, `delete` e `save` ([doc oficial, linha 5](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L5)).

| Operador | Magic method | Exemplo PyODMongo | MongoDB equivalente | Referência |
|---|---|---|---|---|
| Equal | `Product.name == 'Box'` | `Product.name.eq('Box')` | `{name: {$eq: "Box"}}` | [L10](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L10) |
| Greater than | `Product.price > 10` | `Product.price.gt(10)` | `{price: {$gt: 10}}` | [L30](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L30) |
| Greater than equal | `Product.price >= 10` | `Product.price.gte(10)` | `{price: {$gte: 10}}` | [L50](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L50) |
| In | — | `Product.name.in_(['Ball', 'Box'])` | `{name: {$in: [...]}}` | [L70](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L70) |
| Lower than | `Product.price < 10` | `Product.price.lt(10)` | `{price: {$lt: 10}}` | [L84](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L84) |
| Lower than equal | `Product.price <= 10` | `Product.price.lte(10)` | `{price: {$lte: 10}}` | [L104](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L104) |
| Not equal | `Product.name != 'Box'` | `Product.name.ne('Box')` | `{name: {$ne: "Box"}}` | [L124](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L124) |
| Not in | — | `Product.name.nin(['Ball', 'Box'])` | `{name: {$nin: [...]}}` | [L144](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L144) |
| And | `&` | `and_(cond1, cond2)` | `{$and: [...]}` | [L158](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L158) |
| Or | `\|` | `or_(cond1, cond2)` | `{$or: [...]}` | [L178](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L178) |
| Nor | — | `nor_(cond1, cond2)` | `{$nor: [...]}` | [L198](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L198) |
| Elem match | — | `Product.tags.elem_match(...)` | `{$elemMatch: {...}}` | [L212](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L212) |
| Sort | — | `sort([('name', 1), ('price', -1)])` | `{name: 1, price: -1}` | [L226](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md#L226) |

Exemplo:

```python
product = await engine.find_one(Product, Product.price >= 10)
products = await engine.find_many(Product, and_(Product.price > 10, Product.price <= 50))
```

## Índices

### Criação simples

A maneira mais simples de criar índices é usando o `Field`, especificando qual campo deve ser indexado ([doc oficial, linha 7](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L7)):

```python
from pydantic import Field

class Product(DbModel):
    name: str = Field(index=True, unique=True)
    description: str = Field(text_index=True, default_language='portuguese')
    _collection: ClassVar = 'products'
```

- `index: bool` — Cria um índice no campo. [L13](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L13)
- `unique: bool` — Índice único (não permite valores duplicados). [L14](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L14)
- `text_index: bool` — Inclui o campo em índices de texto (busca full-text). [L15](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L15)
- `default_language: str` — Idioma padrão do índice de texto. [L16](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L16)

### Criação avançada

Para índices mais específicos, use `IndexModel` do PyMongo no atributo de classe `_indexes` ([doc oficial, linha 20](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L20)):

```python
from pymongo import IndexModel, ASCENDING, DESCENDING

class Product(DbModel):
    name: str
    price: float
    product_type: str
    _collection: ClassVar = 'products'
    _indexes = [
        IndexModel([('name', ASCENDING), ('price', DESCENDING)], name='name_and_price'),
        IndexModel([('product_type', DESCENDING)], name='product_type'),
    ]
```

O PyODMongo oferece suporte à criação de qualquer estrutura de índice seguindo as diretrizes do PyMongo. ([doc oficial, linha 30](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md#L30))

## Aggregation

Para utilizar pipelines de agregação, defina o atributo de classe `_pipeline` no modelo. Ao chamar `find_one` ou `find_many`, a biblioteca executa o pipeline e retorna o resultado como objetos Python ([doc oficial, linha 7](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/aggregation.md#L7)):

```python
class OrdersByCustomers(DbModel):
    _id: str
    count: int
    total: float
    _collection: ClassVar = 'orders'
    _pipeline = [
        {
            '$group': {
                '_id': '$customer_id',
                'count': {'$sum': 1},
                'total': {'$sum': '$value'}
            }
        }
    ]
```

> **Dica**: O PyODMongo já usa agregação internamente em `find`/`find_one`. O parâmetro `query` é convertido em um estágio `$match` inserido como a primeira etapa do pipeline. A saída do pipeline deve estar alinhada com os campos da classe. ([doc oficial, linha 23](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/aggregation.md#L23))

## Uso com FastAPI

O PyODMongo é totalmente compatível com FastAPI devido à sua base Pydantic, permitindo criar consultas dinâmicas em tempo de execução ([doc oficial, linha 3](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L3)). A função `mount_query_filter` constrói dinamicamente uma consulta a partir das query strings da requisição ([doc oficial, L9](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L9)):

```python
from fastapi import FastAPI, Request
from pyodmongo import AsyncDbEngine, DbModel, mount_query_filter

app = FastAPI()
engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

@app.get('/')
async def read_items(request: Request):
    query = mount_query_filter(Product, request.query_params._dict)
    return await engine.find_many(Product, query)
```

Ela é compatível com o atributo `request.query_params._dict`, que contém as query strings da rota ([doc oficial, linha 13](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L13)).

### Parâmetros de `mount_query_filter`

- `Model: DbModel` — Modelo para o qual a query será construída. [L17](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L17)
- `items: dict` — Dicionário com os itens de consulta. [L18](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L18)
- `initial_comparison_operators: list[ComparisonOperator]` — Lista inicial de operadores de comparação. [L19](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L19)

A função retorna uma consulta com o operador `and` aplicado entre todos os itens do dicionário ([doc oficial, linha 21](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L21)).

### Formato das query strings

As chaves devem ser o nome do atributo seguido de `_` e de um operador válido (`"eq", "gt", "gte", "in", "lt", "lte", "ne", "nin", "sort"`). ([doc oficial, linha 39](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L39))

Exemplo de URL ([L27](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md#L27)):

```
http://localhost:8000/?attr1_eq=value_1&attr2_in=%5B'value_2',%20'value_3'%5D&attr3_gte=10&_sort=%5B%5B'attr1',%201%5D,%20%5B'attr2',%20-1%5D%5D
```

Dicionário resultante em `request.query_params._dict`:

```python
{
    "attr1_eq": "value_1",
    "attr2_in": "['value_2', 'value_3']",
    "attr3_gte": 10,
    "_sort": "[['attr1', 1], ['attr2', -1]]",
}
```

## Contribuições

Contribuições são bem-vindas. Abra uma issue ou envie uma pull request no [repositório do GitHub](https://github.com/mauro-andre/pyodmongo). ([doc oficial, linha 47](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md#L47))

## Referências (todas as fontes)

- [index.md — Visão geral](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/index.md) — recursos, instalação, licença, contribuições
- [getting_started.md — Primeiros passos](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/getting_started.md) — motor, modelo, save, find_one
- [db_model.md — DbModel](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/db_model.md) — atributos herdados e relacionamentos
- [save.md — Save e DbResponse](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/save.md)
- [find.md — Find, paginação e populate](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/find.md)
- [delete.md — Delete e delete_one](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/delete.md)
- [query_operators.md — Operadores de query](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/query_operators.md)
- [indexes.md — Índices](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/indexes.md)
- [aggregation.md — Aggregation](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/aggregation.md)
- [fastapi.md — Uso com FastAPI](https://github.com/mauro-andre/pyodmongo/blob/master/docs/pt-BR/fastapi.md)