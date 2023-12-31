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

_catagory_dict = {
    "dairy": "Dairy",
    "packaged_goods": "Packaged Goods",
    "canned_goods": "Canned Goods",
    "condiments_sauces": "Condiments & Sauces",
    "drink_beverages": "Drinks & Beverages"
}


class ItemView:
    def __init__(self, item_dict):
        # {
        #     'item_name': 'Milk',
        #     'item_price': 2.3,
        #     'item_catagory': 'dairy',
        #     'item_id': '7026020123126'
        # }
        self._qty: bool = True if "cart_qty" in item_dict else False
        self._inv = item_dict["item_qty"] if "item_qty" in item_dict else 0
        self._item_dict: dict = item_dict
        self.item_name = item_dict["item_name"]
        self.item_price = item_dict["item_price"]
        self.item_catagory = _catagory_dict[item_dict["item_catagory"]]
        self.item_id = item_dict["id"]
        self.item_description = None
        self.item_image = None

    def getName(self):
        return self.item_name

    def getPrice(self):
        return float(self.item_price)

    def getGSTPrice(self):
        return round(float(self.item_price)*1.07, 2)

    def getRounding(self):
        return (self.getPrice()*1.07)-self.getGSTPrice()

    def getCatagory(self):
        return self.item_catagory

    def getDescription(self):
        return self.item_description

    def getImage(self):
        return self.item_image

    def getInventory(self):
        return int(self._inv)

    def set_qty(self, num):
        self._qty = True
        self._item_dict["cart_qty"] = num

    def get_qty(self):
        if self._qty:
            return self._item_dict["cart_qty"]
        else:
            return 0