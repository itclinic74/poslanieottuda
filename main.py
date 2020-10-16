# -*- coding: utf8 -*-
import base64
import json
import requests
from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET', 'PUT'])
def eqwid_pochta_request():
    if request.method == "POST":
        r = request.json
        id = r['entityId']
        id_str = str(id)
        # Данные ecwid
        public_token = 'public_brxHKj2cqjivpDFkvtsBr1A4HXaDH5Em'
        secret_token = 'secret_3fDhxvXSVcryGQr971zbdSD5iWpmfnk2'
        store_id = '21125130'
        # Получение данных о заказе
        url: str = "https://app.ecwid.com/api/v3/" + store_id + "/orders/" + id_str + "?token=" + secret_token
        r = requests.get(url)
        req_data = r.json()
        # Нормализация адреса
        def to_base64(str):
            return base64.b64encode(str.encode()).decode("utf-8")
        # Данные Почты России
        access_token = "urCHr2G7Xa_UgfYn1ldOJ670LKRhL1LR"
        login_password = to_base64("poslanie-ottuda.chek@yandex.ru:poslanieottuda88")
        request_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=UTF-8",
            "Authorization": "AccessToken " + access_token,
            "X-User-Authorization": "Basic " + login_password
        }
        url = 'https://otpravka-api.pochta.ru/1.0/clean/address'
        all_name = req_data['shippingPerson']
        original_address = all_name['city'] + all_name['street']
        raw_address = [
            {
                "id": "adr 1",
                "original-address": original_address
            }
        ]
        norm_response = requests.post(url, headers=request_headers, data=json.dumps(raw_address))
        norm_address = norm_response.json()
        # Данные для отправки на Почту России
        address_type_to = 'DEFAULT'
        items = req_data['items']
        items_1 = items[0]
        given_name = all_name['firstName'] # Имя
        dict_address = norm_address[0]
        house_to = dict_address['house'] # Номер дома
        index_to = all_name['postalCode'] # Индекс получателя
        mail_category = 'ORDINARY' # Уточнить категорию РПО
        mail_direct = '643' # Код страны
        mail_type = 'ONLINE_PARCEL' # Вид отправления (уточнить)
        mass = items_1['weight']  # Поменять массу нужно принимать от магазина в JSON
        order_num = req_data['id']
        place_to = all_name['city'] # Город
        postoffice_code = '102961' # Индекс отделения-отправителя
        region_to = all_name['stateOrProvinceName'] # Область
        room_to = dict_address['room'] # Квартира
        street_to = dict_address['street']  # Улица
        surname = all_name['lastName'] # Фамилия
        tel_address = all_name['phone'] # Телефон
        new_order = [
            {
                "address-type-to": address_type_to,
                "given-name": given_name,
                "house-to": house_to,
                "index-to": index_to,
                "mail-category": mail_category,
                "mail-direct": mail_direct,
                "mail-type": mail_type,
                "mass": mass,
                "order-num": order_num,
                "postoffice-code": postoffice_code,
                "place-to": place_to,
                "region-to": region_to,
                "room-to": room_to,
                "street-to": street_to,
                "surname": surname,
                "tel-address": tel_address
            }
        ]
        protocol = "https://"
        host = "otpravka-api.pochta.ru"
        path = "/1.0/user/backlog"
        url = protocol + host + path
        # Отправка на Почту России
        response = requests.put(url, headers=request_headers, data=json.dumps(new_order))
        return 'Response: {}'.format(response.text)
    return "Недопустипый запрос"


if __name__ == '__main__':
    app.run()

