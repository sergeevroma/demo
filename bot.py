import config
import telebot
import json

options = {"Поиск в магазине Пятёрочка": 1, "Поиск в магазине Магнит": 2, "Поиск в магазине Перекрёсток": 3,
           "Поиск во всех магазинах": 4}
option = 0


#  Поиск продукта в магазине Магнит
def get_data_magnit(product):
    req, result = {}, ""
    with open(r"magnit.json", "r", encoding="utf-8") as file:
        data = json.loads(file.read())
        for name in data.keys():
            if product.lower() in name.lower():
                req[name] = {"old_price": data[name]["old_price"], "new_price": data[name]["new_price"]}

    if len(req) == 0:
        result = "В магазине <b>'Магнит'</b> нет скидки на введённый продукт"
        return result
    else:
        result = "Возможные товары  из магазина <i><b>'Магнит'</b></i>\n"
        for name, prices in req.items():
            result += f"<b><i>{name}</i></b>\nЦена без скидки: <i>{prices['old_price']}</i> рублей\nЦена со скидкой: <i>{prices['new_price']}</i> рублей\n"
            if len(result) > 4096:
                result = "Извините, найдено слишком много продуктов для магазина <b>'Магнит'</b>.Введите более конкретный запрос",
                return result
    return result


# Поиск продукта в магазине Перекрёсток
def get_data_perekrestok(product):
    req, result = {}, ""
    with open(r"perekrestok.json", "r", encoding="utf-8") as file:
        data = json.loads(file.read())
        for name in data.keys():
            if product.lower() in name.lower() and data[name]["old_price"] != "No.ne":
                req[name] = {"old_price": data[name]["old_price"], "new_price": data[name]["new_price"]}

    if len(req) == 0:
        result = "В магазине <b>'Перекрёсток'</b> нет скидки на введённый продукт"
        return result
    else:
        result = "Возможные товары  из магазина <i><b>'Перекрёсток'</b></i>\n"
        for name, prices in req.items():
            result += f"<b><i>{name}</i></b>\nЦена без скидки: <i>{prices['old_price']}</i> рублей\nЦена со скидкой: <i>{prices['new_price']}</i> рублей\n"
            if len(result) > 4096:
                result = "Извините, найдено слишком много продуктов для магазина <b>'Перекрёсток'</b>.Введите более конкретный запрос",
                return result
    return result


# Поиск продукта в магазине Пятёрочка
def get_data_pyaterochka(product):
    req = {}
    with open(r"pyaterochka.json", "r", encoding="utf-8") as file:
        data = json.loads(file.read())
        for name in data.keys():
            if product.lower() in name.lower():
                req[name] = {"old_price": data[name]["old_price"], "new_price": data[name]["new_price"]}

    if len(req) == 0:
        result = "В магазине <b>'Пятёрочка'</b> нет скидки на введённый продукт"
        return result
    else:
        result = "Возможные товары  из магазина <i><b>'Пятёрочка'</b></i>\n"
        for name, prices in req.items():
            result += f"<b><i>{name}</i></b>\nЦена без скидки: <i>{prices['old_price']}</i> рублей\nЦена со скидкой: <i>{prices['new_price']}</i> рублей\n"
            if len(result) > 4096:
                result = "Извините, найдено слишком много продуктов для магазина <b>'Пятёрочка'</b>.Введите более конкретный запрос",
                return result
    return result


# Телеграмм бот
def telegram_bot():
    bot = telebot.TeleBot(config.token, skip_pending=True)
    markup = telebot.types.ReplyKeyboardMarkup()
    button_A = telebot.types.KeyboardButton(text="Поиск в магазине Пятёрочка")
    button_B = telebot.types.KeyboardButton(text="Поиск в магазине Магнит")
    button_C = telebot.types.KeyboardButton(text="Поиск в магазине Перекрёсток")
    button_D = telebot.types.KeyboardButton(text="Поиск во всех магазинах")
    markup.row(button_A, button_B)
    markup.row(button_C, button_D)

    # Выбор магазина
    @bot.message_handler(commands=["start", "help"])
    def start(message):
        bot.send_message(message.chat.id, config.greetings, reply_markup=markup)

    # Обработка названия магазина и запрос названия товара
    @bot.message_handler(func=lambda message: message.text in options)
    def choose_store(message):
        global option
        option = options[message.text]
        bot.send_message(message.chat.id, config.text1)

    # Получение названия товара, обработка данных и вывод результатов
    @bot.message_handler(content_types=["text"])
    def result(message):
        product_name = message.text  # название продукта
        magnit_data = get_data_magnit(product_name)  # данные с магнита
        perekrestok_data = get_data_perekrestok(product_name)  # данные с перекрёстка
        pyaterochka_data = get_data_pyaterochka(product_name)  # данные с пятёрочки
        if option == 1:
            bot.send_message(message.chat.id, pyaterochka_data, reply_markup=markup, parse_mode="html")
        elif option == 2:
            bot.send_message(message.chat.id, magnit_data, reply_markup=markup, parse_mode="html")
        elif option == 3:
            bot.send_message(message.chat.id, perekrestok_data, reply_markup=markup, parse_mode="html")
        elif option == 4:
            bot.send_message(message.chat.id, pyaterochka_data, parse_mode="html")
            bot.send_message(message.chat.id, magnit_data, parse_mode="html")
            bot.send_message(message.chat.id, perekrestok_data, reply_markup=markup, parse_mode="html")

    bot.polling(none_stop=True)


if __name__ == "__main__":
    telegram_bot()
