from pyodmongo import AsyncDbEngine, DbModel
from pymongo import MongoClient
from typing import ClassVar
import asyncio


engine = AsyncDbEngine(
    mongo_uri='mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000',
    db_name='mongosh+2.5.0'

)

class Produtos(DbModel):
    nome: str
    preco: float
    _collection: ClassVar = 'products'

async def main():
    box = Produtos(nome='Box', preco=5.99)
    result = await engine.save(box)
    print(f'Salvo com id: {result.id }')

asyncio.run(main())