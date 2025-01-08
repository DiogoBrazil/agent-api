from typing import List
from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function
from src.repositories.product_repository import ProductRepository
import asyncio

products = {
    'total_products': None,
    'products': None,
    'products_all': None
}

class ProductTools():

    def __init__(self):
        self.product_repository = ProductRepository()

    async def initialize_get_all_products(self):
        """Inicializa os dados necessários para as tools"""
        global products
        if products['products_all'] is None:
            products['products_all'] = await self.product_repository.get_all_products()
    
    async def initialize_get_total_quantity_of_products(self):
        """Inicializa os dados necessários para as tools"""
        global products
        if products['total_products'] is None:
            products['total_products'] = await self.product_repository.get_total_products()
    
    async def initialize_get_products(self, words: List):
        """Inicializa os dados necessários para as tools"""
        global products
        if len(words) == 0:
            products['products'] = 'Produto não encontrado'
        elif len(words) > 1:
            products['products'] = await self.product_repository.get_product_by_two_or_more_words(words)
        else:
            products['products'] = await self.product_repository.get_product_by_one_word(words)
    

    @staticmethod
    @tool
    def get_all_products() -> str:
        """Faz a busca de todos os produtos cadastrados"""
        global products
        if products['products_all'] is None:
            return "Dados ainda não inicializados"
        return products['products_all']
    
    @staticmethod
    @tool
    def get_total_quantity_of_products() -> str:
        """Faz a busca da quantidade total de produtos cadastrados"""
        global products
        if products['total_products'] is None:
            return "Dados ainda não inicializados"
        return products['total_products']
    
    @staticmethod
    @tool
    def get_products_by_params() -> str:
        """
           Busca informações sobre produtos no catálogo quando o usuario passar a categoria 
           ou nome do produto.
        """
        global products
        if products['products'] is None:
            return "Nenhum produto encontrado"
        return products['products']
    
    def return_tools(self):
        tools = [self.get_all_products, self.get_total_quantity_of_products, self.get_products_by_params]
        return {
            'tools_json': [convert_to_openai_function(tool) for tool in tools],
            'tool_run': {tool.name: tool for tool in tools}
        }