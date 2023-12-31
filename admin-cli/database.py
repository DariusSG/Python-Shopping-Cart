#  Copyright (C) 2022 DariusSG
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import functools
from functools import reduce
from random import randrange

from tinydb_encrypted_jsonstorage.encrypted_json_storage import EncryptedJSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware
from tinydb.operations import add
import tinydb

from datetime import datetime

class Constants:
    CATAGORY = ["dairy", "packaged_goods", "canned_goods", "condiments_sauces", "drink_beverages"]
    item_list = [
        {
            'item_name': 'Milk',
            'item_price': 2.3,
            'item_catagory': 'dairy',
            'item_id': '7026020123126'
        },
        {
            'item_name': 'Butter',
            'item_price': 4.5,
            'item_catagory': 'dairy',
            'item_id': '1027582532179'
        },
        {
            'item_name': 'Eggs',
            'item_price': 3.4,
            'item_catagory': 'dairy',
            'item_id': '2579692860103'
        },
        {
            'item_name': 'Cheese Slices',
            'item_price': 3.15,
            'item_catagory': 'dairy',
            'item_id': '0015981529310'
        },
        {
            'item_name': 'Evaporated Milk Creamer',
            'item_price': 1.4,
            'item_catagory': 'dairy',
            'item_id': '7797200036450'
        },
        {
            'item_name': 'Milo',
            'item_price': 12.5,
            'item_catagory': 'dairy',
            'item_id': '6476204540750'
        },
        {
            'item_name': 'Biscuits',
            'item_price': 5.3,
            'item_catagory': 'dairy',
            'item_id': '9600664653478'
        },
        {
            'item_name': 'Yogurt',
            'item_price': 0.95,
            'item_catagory': 'dairy',
            'item_id': '1766272847833'
        },
        {
            'item_name': 'Bread',
            'item_price': 2.7,
            'item_catagory': 'packaged_goods',
            'item_id': '5956927258534'
        },
        {
            'item_name': 'Cereal',
            'item_price': 7,
            'item_catagory': 'packaged_goods',
            'item_id': '3828500589576'
        },
        {
            'item_name': 'Crackers',
            'item_price': 3.1,
            'item_catagory': 'packaged_goods',
            'item_id': '2406646539122'
        },
        {
            'item_name': 'Chips',
            'item_price': 2.6,
            'item_catagory': 'packaged_goods',
            'item_id': '4205581475865'
        },
        {
            'item_name': 'Raisin',
            'item_price': 2.1,
            'item_catagory': 'packaged_goods',
            'item_id': '5765483831996'
        },
        {
            'item_name': 'Nuts',
            'item_price': 2,
            'item_catagory': 'packaged_goods',
            'item_id': '3567325289154'
        },
        {
            'item_name': 'Green_beans',
            'item_price': 1.05,
            'item_catagory': 'packaged_goods',
            'item_id': '7207518808033'
        },
        {
            'item_name': 'Barley',
            'item_price': 1.05,
            'item_catagory': 'packaged_goods',
            'item_id': '7357399476804'
        },
        {
            'item_name': 'Tomato',
            'item_price': 1.45,
            'item_catagory': 'canned_goods',
            'item_id': '2563595658080'
        },
        {
            'item_name': 'Button Mushroom',
            'item_price': 1.15,
            'item_catagory': 'canned_goods',
            'item_id': '1564784858152'
        },
        {
            'item_name': 'Baking Bean',
            'item_price': 1.35,
            'item_catagory': 'canned_goods',
            'item_id': '5175550741712'
        },
        {
            'item_name': 'Tuna Fish',
            'item_price': 1.45,
            'item_catagory': 'canned_goods',
            'item_id': '1532210156882'
        },
        {
            'item_name': 'Kernel Corn',
            'item_price': 1.25,
            'item_catagory': 'canned_goods',
            'item_id': '3724570299172'
        },
        {
            'item_name': 'Sardine Fish',
            'item_price': 1.1,
            'item_catagory': 'canned_goods',
            'item_id': '9525145401525'
        },
        {
            'item_name': 'Chicken Luncheon Meat',
            'item_price': 1.95,
            'item_catagory': 'canned_goods',
            'item_id': '0409155624589'
        },
        {
            'item_name': 'Pickled Lettuce',
            'item_price': 0.95,
            'item_catagory': 'canned_goods',
            'item_id': '0585169219482'
        },
        {
            'item_name': 'Fine Salt',
            'item_price': 0.8,
            'item_catagory': 'condiments_sauces',
            'item_id': '4216410453480'
        },
        {
            'item_name': 'Sea Salt Flakes',
            'item_price': 1.3,
            'item_catagory': 'condiments_sauces',
            'item_id': '3284471022557'
        },
        {
            'item_name': 'Chicken Stock',
            'item_price': 3.15,
            'item_catagory': 'condiments_sauces',
            'item_id': '5304607038042'
        },
        {
            'item_name': 'Chilli Sauce',
            'item_price': 2.65,
            'item_catagory': 'condiments_sauces',
            'item_id': '2872384474368'
        },
        {
            'item_name': 'Oyster Sauce',
            'item_price': 4.5,
            'item_catagory': 'condiments_sauces',
            'item_id': '9385812559474'
        },
        {
            'item_name': 'Sweet Soy Sauce',
            'item_price': 3.75,
            'item_catagory': 'condiments_sauces',
            'item_id': '3784513977345'
        },
        {
            'item_name': 'Tomato Ketchup',
            'item_price': 3.2,
            'item_catagory': 'condiments_sauces',
            'item_id': '2474406913048'
        },
        {
            'item_name': 'Sesame Oil',
            'item_price': 4.95,
            'item_catagory': 'condiments_sauces',
            'item_id': '7853408150944'
        },
        {
            'item_name': 'Green Tea Canned 330 ML',
            'item_price': 15,
            'item_catagory': 'drink_beverages',
            'item_id': '7975389484839'
        },
        {
            'item_name': 'Blackcurrant Ribena 330 ML',
            'item_price': 31,
            'item_catagory': 'drink_beverages',
            'item_id': '4393156172407'
        },
        {
            'item_name': '100 Plus 24 Cans',
            'item_price': 15, 'item_catagory': 'drink_beverages',
            'item_id': '0180746267742'
        },
        {
            'item_name': 'Orange Cordial 2 Litre',
            'item_price': 3.9,
            'item_catagory': 'drink_beverages',
            'item_id': '9841307284004'
        },
        {
            'item_name': 'Mineral Water 24 x 600 ML',
            'item_price': 7,
            'item_catagory': 'drink_beverages',
            'item_id': '5439268318278'
        },
        {
            'item_name': 'Pineapple juice',
            'item_price': 0.8,
            'item_catagory': 'drink_beverages',
            'item_id': '1843549667056'
        },
        {
            'item_name': 'Nescafe Coffee',
            'item_price': 9.9,
            'item_catagory': 'drink_beverages',
            'item_id': '8386063837114'
        },
        {
            'item_name': 'Coke 24 Cans',
            'item_price': 12.4,
            'item_catagory': 'drink_beverages',
            'item_id': '2961344569371'
        }
    ]
    discount_card_nums = [
        "7WB8242PMQPHPIG0QOPBBOBNL",
        "ZVP044H9S9EJADJOVEC55TTJA",
        "8E0VBN3OF24HJG0LQ579HUM6Y",
        "OQ6RD4YJMXH2EZ6326F89R1DO",
        "HGVPDPTJQSTDP9X601REGGPBX",
        "7UB7HMHX0TXAXD15HTMQ8UCX9",
        "WIW0U7QNS9PLKZASCRI6AQV86",
        "EIRBSOYGSEJGE7E8FUBABMMRN",
        "NTS6H0OQQFV0UTUSTN6SWZLE6",
        "CRFN70YCG7MPBU64B9W1MADBU",
        "H0KXM8LXZHOVZGN3ZCIQVH7R8",
        "CFO8VK03VZNAFNYFQAMP81OYD",
        "3UITZA2C1NV6WFV6YJYB9KKTF",
        "8PMBW0LA03H4J7BJMH81R4KJU",
        "ZX7FJZTK4CJPP3D31FQ5LDJ0G",
        "TVLRRX6T79KLHD1O7RE0D7WAT",
        "9XXN19MZ9RJ8SKM5NGPGQ4OIQ",
        "FX4K3OADV75Z6FMMUNR2MGAXX",
        "L5DE8EZO7UACGWAL9ISNFGL5N",
        "RUYVS1KJOAJ1MMHXHJS3MG05O",
        "2OJHXG7FEWKIZOZVJQ806YD7T",
        "O2330L6TGYVM948T36JH60GM2",
        "73RHQE4SI4F7Y0YZW0YHN978T",
        "IOSGPX8BD7UFGHZ38LQ0B3KEZ",
        "DTEMLTIZ89GKSJC26GZFA8OY8"
    ]


class InvaildSearchFilter(Exception):
    pass


class InvaildItemParam(Exception):
    pass


class DatabaseUpdateFailed(Exception):
    pass


class DatabaseSearchFailed(Exception):
    pass


class DatabaseInsertFailed(Exception):
    pass


def generate_EAN13():
    numbers = [randrange(10) for _ in range(12)]

    evensum = reduce(lambda x, y: int(x) + int(y), numbers[::2])
    oddsum = reduce(lambda x, y: int(x) + int(y), numbers[1::2])
    numbers.append((10 - ((evensum + oddsum * 3) % 10)) % 10)

    return ''.join(map(str, numbers))


class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj: datetime):
        return obj.strftime("%d;%m;%Y-%w-%H:%M")

    def decode(self, string: str):
        return datetime.strptime(string, "%d;%m;%Y-%w-%H:%M")


class main_Database:
    def __init__(self, path_to_file,key):
        serialization = SerializationMiddleware(EncryptedJSONStorage)
        serialization.register_serializer(DateTimeSerializer(), 'OBJ_datetime')
        self._db = tinydb.TinyDB(encryption_key=key, path=path_to_file, storage=serialization)

    def get_item_database(self):
        return item_Table(self._db)

    def get_sales_database(self):
        return sales_Table(self._db)

    def close(self):
        self._db.close()


class item_Table:
    CATAGORY = ["dairy", "packaged_goods", "canned_goods", "condiments_sauces", "drink_beverages"]

    def __init__(self, path_to_file):
        self._db = path_to_file.table("item_table")

    @functools.lru_cache(maxsize=256)
    def search(self, search_name: str, item_catagory: str = None, item_price_asc: bool = True,
               item_name_asc: bool = True, return_dict: bool = False):
        search_filters = {"catagory": item_catagory, "price_op": not item_price_asc, "name_op": not item_name_asc}

        if search_name is not None:
            if search_filters.get("catagory") is None:
                search_result = self._db.search(tinydb.Query().item_name.search(search_name))

            elif search_filters.get("catagory") in self.CATAGORY:
                search_result = self._db.search(
                    (
                            tinydb.Query().item_catagory == search_filters.get("catagory")
                    ) & (
                            tinydb.Query().item_name.search(search_name)
                    )
                )
            else:
                raise InvaildSearchFilter("Catagory does not exists")
        else:
            if search_filters.get("catagory") is None:
                search_result = self._db.all()

            elif search_filters.get("catagory") in self.CATAGORY:
                search_result = self._db.search(
                    tinydb.Query().item_catagory.search == search_filters.get("catagory")
                )

            else:
                raise InvaildSearchFilter("Catagory does not exists")


        search_result = sorted(search_result, key=lambda d: d["item_price"], reverse=search_filters.get("price_op"))

        return sorted(search_result, key=lambda d: d["item_name"], reverse=search_filters.get("name_op"))


    def add_item(self, item_name: str, item_catagory: str, item_price: float, item_barcode: str):
        if type(item_name) != str or type(item_catagory) != str or not(type(item_price) == float or type(item_price) == int) or type(item_barcode) != str:
            raise InvaildItemParam(f"Item missing required param")
        else:
            try:
                self._db.insert({
                    "item_name": item_name,
                    "item_catagory": item_catagory,
                    "item_price": item_price,
                    "item_qty": 0,
                    "id": item_barcode
                })
            except Exception as err:
                raise DatabaseInsertFailed(f"Failed to insert item\nError: {err}")

    def add_inventory(self, item_barcode: str, item_qty: int):
        try:
            query = tinydb.Query()
            self._db.update(
                add("item_qty", item_qty),
                query.id == item_barcode
            )
        except Exception as err:
            raise DatabaseUpdateFailed(f"Failed to update item\nError: {err}")

    def getItembyID(self, item_id):
        return self._db.get(tinydb.Query().id == item_id)


class sales_Table:
    def __init__(self, path_to_file):
        self._db = path_to_file.table("sales_table")

    def add_customer_sale(self, insert_dict: dict):
        self._db.insert(insert_dict)

    def getSales(self, startrange: datetime, endrange: datetime):
        return self._db.search(startrange <= tinydb.Query().timestamp <= endrange)
