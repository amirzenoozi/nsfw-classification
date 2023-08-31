import numpy as np
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from pathlib import Path
import os
import bot

from keras.models import load_model
from script import utils as instruments


router = Router()


@router.message(Command("start"))
async def start_message(message: Message):
    await message.answer(
        text="Hi there. This bot can recognize NSFW level of pictures you send to it."
    )


@router.message(F.photo)
async def analyze_photo(message: Message):
    await message.reply("Analyzing...")
    file_id = message.photo[-1].file_id
    file = await bot.bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("../media/", f"{file_id}.jpeg")
    await bot.bot.download_file(file_path, destination=file_on_disk)

    model = load_model(
        "/home/capybara/dev/github/nsfw-classification-aiogram/aiogram-base/model/model.h5"
    )
    image = instruments.load_image(file_on_disk.__str__())
    ans = model.predict(image)
    maping = {0: "Neutral", 1: "Porn", 2: "Sexy"}
    new_ans = np.argmax(ans[0])

    await message.reply(
        text=f"``` \nImage Class: {maping[new_ans]} \nProbability {round((ans[0][new_ans] * 100), 2)}% \n```",
        parse_mode="Markdown",
    )

    os.remove(file_on_disk)
