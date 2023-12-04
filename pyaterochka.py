import requests
import json
import schedule


# Парсинг данных
def scraping():
    products = {}
    url = "https://5ka.ru/api/v2/special_offers/?records_per_page=15&store=G014&ordering=&price_promo__gte=&price_promo__lte=&categories=&search=&page=1"
    while True:
        if url is None:
            break
        response = requests.get(url)
        data = response.json()
        for el in data["results"]:
            name = el["name"]
            new_price = el["current_prices"]["price_promo__min"]
            old_price = el["current_prices"]["price_reg__min"]
            products[name] = {"old_price": old_price, "new_price": new_price}
        url = data["next"]
    if len(products) > 0:
        with open("pyaterochka.json", 'w', encoding="utf-8") as file:
            json.dump(products, file, indent=4, ensure_ascii=False)
        print("Successfully")
    else:
        print("Some problems")


def main():
    schedule.every().hour.do(scraping)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()