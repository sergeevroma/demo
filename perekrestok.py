import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import schedule


def scraping():

    # Получение Cookie

    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get("https://www.perekrestok.ru/cat/d")


    cookies = driver.get_cookies()
    s, auth = [], ''
    for cookie in cookies:
        s.append(cookie["name"] + "=" + cookie["value"])
        if cookie["name"] == "session":
            data = json.loads(cookie["value"][2:])
            auth = data["accessToken"]


    # Начальные данные
    page = 1
    headers = {'Content-Type': 'application/json',
                   'Cookie': "; ".join(s),
                   'Auth': 'Bearer ' + auth
                   }
    url = "https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/product/feed"
    f = True
    products = {}

    while f:
        payload = json.dumps({
            "page": page,
            "perPage": 48,
            "filter": {
                "promoListing": 1
            },
            "withBestProductReviews": False
         })
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()
        if not data["content"]["paginator"]["nextPageExists"]:
            f = False
        for product in data["content"]["items"]:
            name = product["title"]
            old_price = str(product["priceTag"]["grossPrice"])
            old_price = old_price[:-2] + "." + old_price[-2:]
            new_price = str(product["priceTag"]["price"])
            new_price = new_price[:-2] + "." + new_price[-2:]
            products[name] = {"old_price": old_price, "new_price": new_price}
        page += 1


    driver.close()
    driver.quit()

    if len(products) > 0:
        with open("perekrestok.json", "w", encoding="utf-8") as file:
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
