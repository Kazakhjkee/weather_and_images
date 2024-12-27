import os
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup

def download_images_requests():
    url = "https://picsum.photos/id/237/200/300"
    os.makedirs("images_requests", exist_ok=True)
    for i in range(1, 11):
        response = requests.get(url)
        with open(f"images_requests/image_{i}.jpg", "wb") as file:
            file.write(response.content)
    print("Картинки скачаны с использованием requests!")

async def download_image_aiohttp(session, url, folder, index):
    async with session.get(url) as response:
        content = await response.read()
        with open(f"{folder}/image_{index}.jpg", "wb") as file:
            file.write(content)

async def download_images_aiohttp():
    url = "https://picsum.photos/200/300"
    os.makedirs("images_aiohttp", exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_image_aiohttp(session, url, "images_aiohttp", i)
            for i in range(1, 11)
        ]
        await asyncio.gather(*tasks)
    print("Картинки скачаны с использованием aiohttp!")

def save_images_in_folders(folder="images_requests"):
    for i in range(1, 11):
        subfolder = f"folder_{i}"
        os.makedirs(subfolder, exist_ok=True)
        source_path = f"{folder}/image_{i}.jpg"
        dest_path = f"{subfolder}/image_{i}.jpg"
        os.rename(source_path, dest_path)
    print("Картинки сохранены в разные папки!")

def get_weather_split():
    url = "https://worldweather.wmo.int/en/home.html"  # Пример сайта
    response = requests.get(url)
    html = response.text

    parts = html.split("Astana")
    if len(parts) > 1:
        weather_info = parts[1].split("<")[0]
        print("Погода в Астане (split):", weather_info.strip())
    else:
        print("Не удалось найти информацию о погоде.")

def get_weather_bs4():
    url = "https://www.accuweather.com/en/kz/kyzylorda/225449/weather-forecast/225449"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    weather_element = soup.find(text="Kyzylorda")
    if weather_element:
        print("Погода в Кызылорде (BeautifulSoup):", weather_element.strip())
    else:
        print("Не удалось найти информацию о погоде.")


def main():
    print("=== Часть 1: Загрузка картинок ===")
    download_images_requests()

    asyncio.run(download_images_aiohttp())

    save_images_in_folders(folder="images_requests")

    print("\n=== Часть 2: Парсинг погоды ===")
    get_weather_split()

    get_weather_bs4()

if __name__ == "__main__":
    main()
