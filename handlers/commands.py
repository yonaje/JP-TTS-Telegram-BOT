from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(
        f"Its simple telegram bot that allows you to create voice messages with VOICEVOX's characters voices\n\n"
        f"By default you have Shikoku Metan's voice, you can change it by /character comamnd\n\n"
        f"What's VOICEVOX or some other stuff you can check /info"
    )
