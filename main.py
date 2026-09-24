import os
from typing import ClassVar
import uvicorn
from fastapi import FastAPI
from pyodmongo import AsyncDbEngine, DbModel
from pymongo import MongoClient

app = FastAPI(title='MongoDB API', version='1.0.0')

MONGO_URI = 'mongodb+srv://edigelson59797686_db_user:TKCwbPEpujpdQBzj@senac.cveqazu.mongodb.net/?appName=Senac'
DB_NAME = 'Senac'

engine = AsyncDbEngine(mongo_uri=MONGO_URI, db_name=DB_NAME)


class Produtos(DbModel):
    nome: str
    preco: float
    _collection: ClassVar = 'products'


def check_connection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        client.admin.command('ping')
        return True, None
    except Exception as e:
        return False, str(e)[:300]


@app.get('/')
async def root():
    connected, error = check_connection()
    payload = {'status': 'ok', 'connected': connected}
    if error:
        payload['error'] = error
    return payload


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