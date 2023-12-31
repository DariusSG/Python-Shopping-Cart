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

import csv
from datetime import datetime
from dateutil import rrule
from typing import TYPE_CHECKING

from states.classCart import CartState


class SalesInsertion:
    def __init__(self):
        self._discount = None
        self._roundings = None
        self._order_no = None
        self._timestamp = None
        self._customer_id = None
        self._payable = None
        self._cart = None

    def set_cart(self, cart: CartState):
        self._cart: list = cart.cart_items.copy()

    def set_discount(self, discount_no):
        self._discount: str = discount_no

    def set_customer_id(self, uuid):
        self._customer_id: str = uuid

    def setOrderNumber(self, num):
        self._order_no: str = num

    def set_payable(self, net_payable):
        self._payable: float = net_payable

    def setRoundings(self, checkCart: CartState, discount: bool):
        total = checkCart.getCartTotalwoGST()
        discount_given = round(total * 0.1 if discount else 0, 2)
        total = total - discount_given + 5
        total = total * 1.07
        self._roundings: float = total - self._payable

    def setTimeStamp(self):
        self._timestamp: str = datetime.now().strftime("%d;%m;%Y-%w-%H:%M")

    def gen_insert(self):
        return {
            "order_no": self._order_no,
            "customer_id": self._customer_id,
            "ordered_items": self._cart,
            "discount_no": self._discount,
            "roundings": self._roundings,
            "net_payable": self._payable,
            "timestamp": self._timestamp
        }


# def collect_data(sales_data: list, start_date, end_date):
#     total_sale, daily_sale = {}, {}
#     for sale in sales_data:
#         for item, qty in sale["ordered_items"]:
#             if item in total_sale.keys():
#                 total_sale[item] += qty
#             else:
#                 total_sale[item] = qty
#
#     for day in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
#         daily_sale[day.strftime("%Y-%m-%d")] = {}
#         for sale in sales_data:
#             if sale["timestamp"].date() == day.date():
#                 for item, qty in sale["ordered_items"]:
#                     if item in total_sale.keys():
#                         daily_sale[day.strftime("%Y-%m-%d")][item] += qty
#                     else:
#                         daily_sale[day.strftime("%Y-%m-%d")][item] = qty
#
#     return total_sale, daily_sale
#
#
# def export_csv(total_sale, daily_sale):
#     fisc_month = datetime.now().strftime("%d-%m-%Y")
#
#     with open(f'./exports/total_sale-{fisc_month}.csv', mode='w') as csv_file:
#         header_field = ["item_id", "qty_sold"]
#         writer = csv.DictWriter(csv_file, fieldnames=header_field)
#         writer.writeheader()
#         for item_id in total_sale:
#             writer.writerow({"item_id": item_id, "qty_sold": total_sale[item_id]})
#
#     for day in daily_sale:
#         with open(f'./exports/daily_sale-{day}.csv', mode='w') as csv_file:
#             header_field = ["item_id", "qty_sold"]
#             writer = csv.DictWriter(csv_file, fieldnames=header_field)
#             writer.writeheader()
#             for item_id in daily_sale[day]:
#                 writer.writerow({"day":"",  "item_id": item_id, "qty_sold": daily_sale[day][item_id]})
