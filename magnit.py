import requests
import json
import schedule



def scraping():
    products = {}
    page = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-app-version': '0.1.0',
        'x-client-name': 'magnit',
        'x-device-id': 'this._deviceld',
        'x-device-tag': 'disabled',
        'x-platform-version': 'window.navigator.userAgent',
    }
    while True:
        url = "https://web-gateway.middle-api.magnit.ru/v1/promotions?limit=36&storeId=9725&sortBy=priority&order=desc&adult=true&offset="+str(page)
        response = requests.get(url, headers=headers)
        data = response.json()
        if len(data["data"]) == 0:
            break
        for product in data["data"]:
            if 'oldPrice' in product:
                name = product["name"]
                old_price = str(product['oldPrice'])
                old_price = old_price[:-2] + "." + old_price[-2:]
                new_price = str(product['price'])
                new_price = new_price[:-2] + "." + new_price[-2:]
                products[name] = {"old_price": float(old_price), "new_price": float(new_price)}
        page += 36
    if len(products) > 0:
        with open("magnit.json", "w", encoding="utf-8") as file:
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
