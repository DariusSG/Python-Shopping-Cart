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

from states.classItem import ItemView
from database import main_Database, item_Table


class CartState:
    def __init__(self, item_database: main_Database):
        self.database: item_Table = item_database.get_item_database()
        self.cart_items: list = []

    def getPos(self, id_item):
        for pos, (id, _) in enumerate(self.cart_items):
            if id == id_item:
                return pos
        return -1

    def addItem(self, item_id: str, qty: int):
        self.cart_items.append((item_id, qty))

    def changeItem(self, item_id: str, new_qty: int):
        if self.cart_items == 0:
            self.cart_items.append((item_id, new_qty))

        self.cart_items[self.getPos(item_id)] = (item_id, new_qty)

    def deleteItem(self, item_id):
        self.cart_items.remove(self.cart_items[self.getPos(item_id)])

    def isEmpty(self):
        return len(self.cart_items) == 0

    def ItemeExists(self, item_id):
        if self.getPos(item_id) == -1:
            return False
        else:
            return True

    def getItemView(self, item_id):
        item_view = ItemView(self.database.getItembyID(item_id))
        item_view.set_qty(self.getItemQty(item_id))
        return item_view

    def getItemQty(self, item_id):
        _, qty = self.cart_items[self.getPos(item_id)]
        return qty

    def getItemTotal(self, item_id):
        return self.getItemView(item_id).getGSTPrice() * self.getItemQty(item_id)

    def getCartTotal(self):
        if self.isEmpty():
            return 0
        total = 0
        for _, (item_id, item_qty) in enumerate(self.cart_items):
            total += self.getItemView(item_id).getGSTPrice() * item_qty
        return total

    def getCartTotalwoGST(self):
        if self.isEmpty():
            return 0
        total = 0
        for _, (item_id, item_qty) in enumerate(self.cart_items):
            total += self.getItemView(item_id).getPrice() * item_qty
        return total

    def genrecipt(self):
        for pos, (item_id, item_qty) in enumerate(self.cart_items):
            item_view = self.getItemView(item_id)
            yield [f"\n{pos+1:02d}. {item_view.getName():<30} Item {item_id:<13s} Price: S${item_view.getGSTPrice():.2f}\n", f"    QTY: {str(item_qty):<3s}   Total: S${item_qty*item_view.getGSTPrice():.2f}"]

    def enumerateCart(self):
        for pos, (item_id, item_qty) in enumerate(self.cart_items):
            item_view = self.getItemView(item_id)
            yield f"{pos+1:02d}. {item_view.getName():<30} Item {item_id:<13s} Price: S${item_view.getGSTPrice():.2f}       {''*35}QTY: {str(item_qty):<3s}   Total: S${item_qty*item_view.getGSTPrice():.2f}"

    def clearCart(self):
        self.cart_items = []