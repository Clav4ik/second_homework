import json

import scrapy
from scrapy.spiders import Spider,Rule
import os
from tutorial.items import AutoItem

import requests
from scrapy.item import Item,Field
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "quotes"



    def start_requests(self):

        res = parse()
        Maybelast = AutoItem


        Maybelast["model"] = res
        #don`t work ;_(
        #I will redo but later
        yield Maybelast



URL = "https://auto.ria.com/uk/legkovie/tesla/"
HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.3"
        "6 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "accept": "*/*",
    }
        # HOST = "https://auto.ria.com"
    # FILE = "cars.csv"

        # yield scrapy.Request(url=URL, headers=HEADERS, callback=self.parse)


def get_html( url, params=None):
        return requests.get(url, headers=HEADERS, params=params)


def get_pages_count( parsed_html):
        pagination = parsed_html.find_all("span", class_="page-item mhide")
        if pagination:
            return int(pagination[-1].get_text())
        else:
             return 1

def get_content( parsed_html):
        items = parsed_html.find_all("div", class_="content")

        cars = []
        for item in items:
            title = item.find("a", class_="address").get_text().split()
            text_for_model = title[:-1]
            model = " ".join(text_for_model)
            year = title[-1]
            try:
                vin = item.find("span", class_="label-vin").text.split()[0]
            except:
                vin = "no VIN"

            cars.append(
                {
                    "model": model,
                    "year": year,
                    "way": item.find("li", class_="item-char js-race").text.split()[0],
                    "uah_price": item.find("span", {"data-currency": "UAH"}).get_text(),
                    "usd_price": item.find("span", {"data-currency": "USD"}).get_text(),
                    "vin": vin,
                    "link": item.find("a", class_="address").get("href")
                }
                 )
        return cars


def save_file( items):
    with open("auto_ria.json", "w", encoding="utf-8") as file:
        json.dump(items, file, indent=2, ensure_ascii=False)


def parse():
    html = get_html(url=URL)
    if html.status_code == 200:
        parsed_html = BeautifulSoup(html.text, "html.parser")
        pages_count = get_pages_count(parsed_html)
        cars = []
        for page in range(1, pages_count + 1):
            print(f"Загрузка {page} из {pages_count}...")
            html = get_html(URL, params={"page": page})
            cars.extend(get_content(parsed_html))
        save_file(cars)

        print(f"Получено {len(cars)} автомобилей!")
        return cars
    else:
            print("Error")


