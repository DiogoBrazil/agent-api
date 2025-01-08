from fastapi import Request
from src.service.chat_service import ChatService

class ChatController:
    def __init__(self):
        self.chatService = ChatService()

    async def input_message(self, input_user):
        return await self.chatService.input_message(input_user)
    
    async def output_message(self):
        return await self.chatService.output_message()