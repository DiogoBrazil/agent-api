from fastapi import HTTPException
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.utils.error_handler import raise_http_error
from src.llm.agent.chat_agent import ChatAgent
import string


class ChatService:
    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.product_repository = ProductRepository()
        self.chat_agent = ChatAgent()

    async def input_message(self, input_user):
        try:
            cleaned_text = input_user.input.translate(str.maketrans('', '', string.punctuation))

            response = await self.chat_agent.run_agent(cleaned_text)

            if not response:
                raise_http_error(404, "Resposta não encontrada")
            
            return {
                "message": "Resposta encontrada",
                "data": response.return_values['output'],
                "status_code": 200
            }
        except HTTPException as http_exc:
            raise http_exc
        
        
    async def output_message(self):
        try:
            products = await self.product_repository.get_all_products()
            products = [product["name"] for product in products]
            if not products:
                 raise_http_error(404, "Produto não encontrado")
            
            return {
                "message": "Produto encontrado",
                "data": products,
                "status_code": 200
            }
        
        except HTTPException as http_exc:
            raise http_exc