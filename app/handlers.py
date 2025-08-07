import tempfile
from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, Voice, CallbackQuery, Chat
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from faster_whisper import WhisperModel

import app.keyboard as kb
from ai_test import query


router = Router()
model = WhisperModel("medium", device="cpu", compute_type="int8")

class Reg(StatesGroup):
    name = State()
    number = State()

class Ai(StatesGroup):
    query = State()

class Dcd(StatesGroup):
    query = State()

class Time(StatesGroup):
    choosedate = State()
    choosetime = State()

# _______________________________________________________________________________________________________________________________________________

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'ку {message.from_user.first_name}.\n /help для инфы.', reply_markup=kb.key_reply)

@router.message(Command('help'))
async def cmd_help(message: Message):
    audio = FSInputFile('utdk/voice_lexin.mp3')
    # await message.answer_audio(audio=audio)
    await message.answer(
        "/reg - зарегаться на крутой конкурс\n"
        "/bot - невероятный чат бот ии умный в очках \n"
        "/buy - поиграть с кнопочками \n"
        "/stt - расшифровка гс или кружка \n\n а пока больше ниче и нет")
    
@router.callback_query(F.data == 'back')
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(f'ку {callback.from_user.first_name}.\n /help для инфы.')

# _______________________________________________________________________________________________________________________________________________

@router.message(Command('buy'))
async def buy_smth(message: Message):
    await message.answer('что вас интересует', reply_markup=kb.shop)

@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("это каталог", reply_markup=await kb.list_of_smth())

@router.callback_query(F.data == 'basket')
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("в корзине ничего нет \n(и не будет, я это не сделал)", reply_markup=kb.setting_for_buttons)

@router.callback_query(F.data == 'pays')
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("скинь 200 рублкй на карту", reply_markup=kb.setting_for_buttons)

@router.callback_query(F.data == 'back_buttons')
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('что вас интересует', reply_markup=kb.shop)

# _______________________________________________________________________________________________________________________________________________

@router.message(Command('reg'))
async def register_1(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("ведите имя")

@router.message(Reg.name)
async def register_2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer("введите номер телефона")

@router.message(Reg.number)
async def register_3(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f"спасибо за регистрацию\n ваше имя - {data['name']}\n телефон - {data['number']}\n вам пизда")
    await state.clear()

# _______________________________________________________________________________________________________________________________________________

@router.message(Command('bot'))
async def ai_command(message: Message, state: FSMContext):
    await state.set_state(Ai.query)
    await message.answer("введите запрос")

@router.message(Ai.query)
async def ai_answer(message: Message, state: FSMContext):
    response = await query(message.text)
    await message.answer(response, parse_mode="Markdown", reply_markup=kb.back)

# _______________________________________________________________________________________________________________________________________________

@router.message(Command('stt'))
async def decoding(message: Message, state: FSMContext):
    await state.set_state(Dcd.query)
    await message.answer("скиньте кружок или гс")

@router.message(Dcd.query, F.voice | F.video_note)
async def cmd_voice(message: Message):
    print(message.video_note)
    if message.voice:
        voice = message.voice
    elif message.video_note:
        voice = message.video_note
    else:
        print('чета пиздарики')
    file = await message.bot.get_file(voice.file_id)
    file_data = await message.bot.download_file(file.file_path)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
        temp_file.write(file_data.read())
        temp_path = temp_file.name
        
    seg, info = model.transcribe(temp_path, language="ru")
    res = ""
    for segment in seg:
        res += segment.text
    await message.answer(res, reply_markup=kb.back)
    print(res)

# _______________________________________________________________________________________________________________________________________________

@router.message(F.text == "Суммаризация (готовые периоды времени) ✨")
async def auto_sum(message: Message, state: FSMContext):
    await sleep(0.3)
    await message.delete()
    await state.set_state(Time.choosetime)
    data = await state.update_data(hrs=12, mins=40, date=F.data)
    print(data)
    await message.answer("соси пока не готово", reply_markup=kb.presets)


@router.message(F.text == "Суммаризация (произвольный период времени) ✨")
async def auto_sum_choosedate(message: Message, state: FSMContext):
    await sleep(0.3)
    await message.delete()
    await state.set_state(Time.choosedate)
    await message.answer("выберите дату для суммаризации",reply_markup=kb.dates)

@router.callback_query(Time.choosedate)
async def auto_sum_choosetime(callback: CallbackQuery, state: FSMContext):
    await sleep(0.3)
    # await message.delete()
    await state.update_data(date=callback.data)
    await state.set_state(Time.choosetime)
    data = await state.update_data(hrs=12, mins=40)
    await callback.message.edit_text("теперь выбери время", reply_markup=kb.summar(data['hrs'], data['mins']))


@router.callback_query(F.data == "hours_minus")
async def hours_minus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["hrs"] = max(0, data.get("hrs") - 1)
    await state.update_data(hrs=data["hrs"])
    await callback.answer()
    await callback.message.edit_text(text="соси пока не готово", reply_markup=kb.summar(data['hrs'], data['mins']))

@router.callback_query(F.data == "hours_plus")
async def hours_plus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["hrs"] = min(23, data.get("hrs") + 1)
    await state.update_data(hrs=data["hrs"])
    await callback.answer()
    await callback.message.edit_text(text="соси пока не готово", reply_markup=kb.summar(data['hrs'], data['mins']))

@router.callback_query(F.data == "minutes_minus")
async def minutes_minus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["mins"] = max(0, data.get("mins") - 5)
    await state.update_data(mins=data["mins"])
    await callback.answer()
    await callback.message.edit_text(text="соси пока не готово", reply_markup=kb.summar(data['hrs'], data['mins']))

@router.callback_query(F.data == "minutes_plus")
async def minutes_plus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["mins"] = min(59, data.get("mins") + 5)
    await state.update_data(mins=data["mins"])
    await callback.answer()
    await callback.message.edit_text(text="соси пока не готово", reply_markup=kb.summar(data['hrs'], data['mins']))


@router.callback_query(F.data == "datetime_next")
async def get_datetime(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text="красава, я обязательно это никуда не запишу")
    await state.clear()

# _______________________________________________________________________________________________________________________________________________

# from db import
# @router.message(F.text)
# async def context_handler(message: Message):

#     await message.answer()