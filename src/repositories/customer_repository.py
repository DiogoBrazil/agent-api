import asyncpg
from typing import List, Dict
from src.infra.database import get_database
from src.config.settings import Settings

class CustomerRepository:
    def __init__(self):
        self.db_connection = get_database()
        self.pool = None
    
    async def init_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(dsn=self.db_connection, min_size=1, max_size=10)

    async def get_customer(self, customer_id: str) -> Dict:
        await self.init_pool()
        try:
            async with self.pool.acquire() as connection:
                customer = await connection.fetchrow(
                    "SELECT * FROM customers WHERE id = $1",
                    customer_id
                )
                if customer:
                    customer_fomated = {
                        "customer_id": customer["id"],
                        "name": customer["name"],
                        "email": customer["email"],
                        "cpf": customer["cpf"],
                        "phone": customer["phone"],       
                    }
                    return customer_fomated
                return None
        except Exception as e:
            print(f"Erro ao buscar cliente: {str(e)}")
            return None
