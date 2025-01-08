from fastapi import APIRouter
from src.controllers.chat_controller import ChatController
from src.interfaces.chat_model import inputUser

router = APIRouter()

chatController = ChatController()

@router.post("/input/")
async def input_message(input_user: inputUser):
    return await chatController.input_message(input_user)

@router.get("/output/")
async def output_message():
    return await chatController.output_message()