import os
from typing import ClassVar

import uvicorn
from fastapi import FastAPI, HTTPException
from pyodmongo import AsyncDbEngine, DbModel
from pymongo import MongoClient

app = FastAPI(title='MongoDB API', version='1.0.0')

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000')
DB_NAME = os.getenv('MONGO_DB', 'mongodb')

engine = AsyncDbEngine(mongo_uri=MONGO_URI, db_name=DB_NAME)


class Produtos(DbModel):
    nome: str
    preco: float
    _collection: ClassVar = 'products'


def check_connection():
    try:
        MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000).admin.command('ping')
        return True
    except Exception:
        return False


@app.get('/')
async def root():
    return {'status': 'ok', 'connected': check_connection()}


@app.post('/products')
async def create_product(nome: str, preco: float):
    produto = Produtos(nome=nome, preco=preco)
    result = await engine.save(produto)
    return {'id': str(result.id), 'nome': nome, 'preco': preco}


@app.get('/products')
async def list_products():
    produtos = await engine.find_many(Produtos, as_dict=True)
    return produtos


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    uvicorn.run(app, host='0.0.0.0', port=port)