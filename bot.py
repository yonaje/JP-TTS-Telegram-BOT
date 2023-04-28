from config import *


dp = Dispatcher()
tr = Translator()


japanese_text = None
@dp.message()
async def echo_handler(message: types.Message) -> None:
        await message.answer(translate_text(message.text))
        japanese_text = translate_text(message.text)
        await create_voice_line(japanese_text)

        audio_from_pc = FSInputFile('voice.wav')
        result = await message.answer_audio(
            audio_from_pc,
            caption=japanese_text
        )


def translate_text(user_input):
    translated_text = tr.translate(user_input, dest='ja').text
    return translated_text


async def create_voice_line(user_input):
    async with Client() as client:
        audio_query = await client.create_audio_query(
            user_input, speaker=10
        )
        with open("voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=10))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())