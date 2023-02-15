import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def star_command(message: types.Message):
    await message.reply(
        "Hello, write me name of city and I'll tell about weather in that city"
    )


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_emoji = {
        "Clear": "clear \U00002600",
        "Clouds": "clouds \U00002601",
        "Rain": "rain \U00002614",
        "Thunderstorm": "thunderstrom \U000026A1",
        "Snow": "snow \U0001F328",
        "Mist": "mist \U0001F32B",
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        weather = data["weather"][0]["main"]
        if weather in code_to_emoji:
            wd = code_to_emoji[weather]
        else:
            wd = "It's hard to say, undefined weather"
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(
            f"\U0000231A {datetime.datetime.now().strftime('%H:%M %d.%m.%Y')} \U0001F4C5\n"
            f"Weather in {city}\U0001F3D9\nTemperature: {int(cur_temp)}C°\U0001F321\nWeather: {wd}\nHumidity: {humidity}%\U0001F4A7\n"
            f"Pressure: {pressure} mmHg\nWind: {int(wind)} m/s\nSunrise time: {sunrise_time.strftime('%H:%M')}\U0001F305\n"
            f"Sunset time: {sunset_time.strftime('%H:%M')}\U0001F307\n*Time is shown in your time zone*\n"
            f"Have a nice day!"
        )
    except:
        await message.reply("\U0001F635Incorrect city, try again\U0001F635")


if __name__ == "__main__":
    executor.start_polling(dp)
