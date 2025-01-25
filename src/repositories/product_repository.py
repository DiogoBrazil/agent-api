import asyncpg
from typing import List, Dict
from src.infra.database import get_database
from src.config.settings import Settings
import requests as req

class ProductRepository:
    def __init__(self):
        self.db_connection = get_database()
        self.pool = None
        self.settings = Settings()
    
    async def init_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(dsn=self.db_connection, min_size=1, max_size=10)

    async def get_total_products(self) -> Dict:
        await self.init_pool()
        try:
            async with self.pool.acquire() as connection:
                quantity_products = await connection.fetchrow(
                    "SELECT COUNT(*) as total_products FROM products"
                )
                print(f'quantity_products: {quantity_products}')
                if quantity_products:
                    return quantity_products["total_products"]
                return 'Não foi possível buscar a quantidade de produtos'
                
        except Exception as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            return None
    
    async def get_product_by_one_word(self, word: List) -> List:
        await self.init_pool()
        try:
            word = word[0]
            async with self.pool.acquire() as connection:
                product = await connection.fetchrow(
                    "SELECT p.name, p.price, p.stock_quantity FROM products p WHERE p.name ILIKE $1",
                    f'%{word}%'
                )
                if product:
                    return product
                return 'Produto não encontrado'
                
        except Exception as e:
            print(f"Erro ao buscar produto por palavra: {str(e)}")
            return
    
    async def get_product_by_two_or_more_words(self, words: List) -> List:
        await self.init_pool()
        try:
            formatted_words = [f'%{word}%' for word in words]
            async with self.pool.acquire() as connection:
                product = await connection.fetch(
                    """SELECT REPLACE(name, '"', '') as name, price,stock_quantity FROM products p WHERE p.name ILIKE ANY ($1)""",
                    formatted_words
                )
                if product:
                    return product
                return 'Produto não encontrado'
                
        except Exception as e:
            print(f"Erro ao buscar produto por palavras: {str(e)}")
            return
        
    async def get_all_products(self) -> List:
        await self.init_pool()
        try:
            async with self.pool.acquire() as connection:
                products = await connection.fetch(
                    "SELECT REPLACE(name, '\"', '') as name FROM products;"
                )
                if products:
                    return products
                return 'Não foi possível buscar os produtos'
                
        except Exception as e:
            print(f"Erro ao buscar todos os produtos: {str(e)}")
            return None
    
    async def get_product_by_description(self, description: str) -> List:
        
        dados = {
            "prompt": description
        }

        headers = {
            'Content-Type': 'application/json',
        }

        print(f"Buscando produto por descrição: {description}")
        print(f"URL: {self.settings.BASE_URL}produtos/prompt")

        response = req.post(f"{self.settings.BASE_URL}produtos/prompt", headers=headers, json=dados)

        if response.status_code == 200:
             return response.json()
        else:
            print(f"Erro ao buscar produto por descrição: {response.text}")
            return None
