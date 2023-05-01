import asyncio

from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile



from data.data import generations
from data.config import selected_generation, selected_character, selected_tone

from googletrans import Translator
from voicevox import Client

tr = Translator()
router = Router()


@router.message(Command('current'))
async def current_settings(message: types.Message):
    await message.answer(
        f'Your character is currently <b>{selected_character}</b> from <b>{selected_generation}</b>.\n'
    )


@router.message(Command('character'))
async def character_select(message: types.Message):

    all_generations = list(generations.keys())

    generation_menu = ReplyKeyboardBuilder()
    for i in range(len(all_generations)):
        generation_menu.add(types.KeyboardButton(text=all_generations[i]))
    generation_menu.adjust(2)

    await message.answer(
        'Select generation',
        reply_markup=generation_menu.as_markup(resize_keyboard = True, one_time_keyboard = True)
    )

    @router.message(F.text.in_(all_generations))
    async def character_select_start(message: types.Message):

        global selected_generation
        selected_generation = message.text

        character_menu = ReplyKeyboardBuilder()
        for i in range(len(generations[selected_generation])):
            character_menu.add(types.KeyboardButton(text=list(generations[selected_generation].keys())[i]))
        character_menu.adjust(2)

        await message.answer(
            selected_generation,
            reply_markup=character_menu.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )

        possible_character = list(generations[selected_generation].keys())

        @router.message(F.text.in_(possible_character))
        async def character_select_finish(message: types.Message):

            global selected_character
            selected_character = message.text
            global selected_tone

            selected_tone = generations[selected_generation][selected_character]['normal']


@router.message(Command("tone"))
async def tone_select(message: types.Message):

    possible_tones = list(generations[selected_generation][selected_character].keys())

    tone_menu = ReplyKeyboardBuilder()
    for i in range(len(possible_tones)):
        tone_menu.add(types.KeyboardButton(text=possible_tones[i]))
    tone_menu.adjust(2)

    await message.answer(
        'Select tone',
        reply_markup=tone_menu.as_markup(resize_keyboard=True, one_time_keyboard = True),
    )

    @router.message(F.text.in_(possible_tones))
    async def tone_select_finish(message: types.Message):

        possible_voices = generations[selected_generation][selected_character]

        global selected_tone
        selected_tone = possible_voices[message.text]


@router.message(Command('voice'))
async def create_voice(message: types.Message, command: CommandObject):

    if command.args:
        user_input = command.args
        async with Client() as client:

            audio_query = await client.create_audio_query(
                tr.translate(user_input, dest='ja').text, speaker=selected_tone
            )

            with open('voice.wav', 'wb') as f:
                f.write(await audio_query.synthesis(speaker = selected_tone))

            await message.answer_voice(
                FSInputFile('voice.wav'), caption='it worked'
            )


    else:

        await message.answer(f'After /voice command, you need to type text \n \n'
        f'/voice <i>some text</i>')



