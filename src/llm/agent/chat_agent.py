from typing import List
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.agent import AgentFinish
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from src.llm.tools.product_tool import ProductTools
from src.utils.finda_similar_word_to_products import find_similar_words_to_get_products
from src.repositories.product_repository import ProductRepository


class ChatAgent():
    def __init__(self):
        self.chat_openai = ChatOpenAI()
        self.tool_product = ProductTools()
        self.product_repository = ProductRepository()
    
    async def initialize_get_all_products(self):
        await self.tool_product.initialize_get_all_products()
    
    async def initialize_get_total_quantity_of_products(self):
        await self.tool_product.initialize_get_total_quantity_of_products()
    
    async def initialize_get_products(self, words: List):
        await self.tool_product.initialize_get_products(words)
    
    def create_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            ('system', 'Você é um assistente amigável chamado Sgt RIbeiro que é responsável por atender clientes, seja para prestar informações de produtos e efetuar compras.'),
            ('user', '{input}'),
            MessagesPlaceholder(variable_name='agent_scratchpad')
        ])
        return prompt
    
    def create_passthrough(self):
        pass_through = RunnablePassthrough.assign(
            agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps'])
        )
        return pass_through
    
    def create_agent_chain(self):
        tools_json = self.tool_product.return_tools()['tools_json']
        agent_chain = (self.create_passthrough() | 
                      self.create_prompt() | 
                      self.chat_openai.bind(functions=tools_json) | 
                      OpenAIFunctionsAgentOutputParser())
        return agent_chain
    
    async def run_agent(self, user_input):
        intermediate_steps = []
        agent_chain = self.create_agent_chain() 
        
        while True:
            response = await agent_chain.ainvoke({
                'input': user_input,
                'intermediate_steps': intermediate_steps
            })
            
            if isinstance(response, AgentFinish):
                return response
            if response.tool == 'get_products_by_params':
                products = await self.product_repository.get_all_products()
                products = [product["name"] for product in products]
                words = find_similar_words_to_get_products(user_input, products)
                await self.initialize_get_products(words)
            else:
                await getattr(self.tool_product, f'initialize_{response.tool}')()

            tool_run = self.tool_product.return_tools()['tool_run']
            observation = tool_run[response.tool].run(response.tool_input)
            intermediate_steps.append((response, observation))