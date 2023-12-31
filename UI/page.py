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

import datetime
import random

import database
import py_tui.colors
from accounting import SalesInsertion
from py_tui import KEY_ENTER, Button
from states.classItem import ItemView
from states.classprofile import UserProfile
from .CustomWidgets import ScrollMenu, CheckBoxMenu
from .common import Page

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from states.classCart import CartState


class itemView(Page):
    def __init__(self, root):
        super().__init__(root, "Item View")
        self.cart_state = self.getGlobalStates().getCartState()
        self.item_id = None
        self.qty = 0
        self.item_view = None
        self.item_price = 0.0
        self.item_name = None
        self.item_catagory = None
        self.total = 0

    def init_page(self):
        super().init_page()
        text_block = self.getWidgetSet().add_text_block("Image", 3, 4, row_span=11, column_span=11)
        self.label = self.getWidgetSet().add_label("", 3, 16, column_span=5)
        self.price = self.getWidgetSet().add_label(f"", 4, 18, column_span=3)
        self.final_price = self.getWidgetSet().add_label(f"", 5, 18, column_span=4)
        self.getWidgetSet().add_label("Delivery QTY", 3, 22, pady=0, column_span=3, padx=0)
        self.add_cart = self.getWidgetSet().add_button("Add to Cart", 5, 22, column_span=3, padx=0, pady=3, command=self.add_to_cart)
        self.cart_qty = self.getWidgetSet().add_label(str(self.qty), 4, 23, pady=1)
        self.cat_label = self.getWidgetSet().add_label(f"Home / {self.item_catagory} / {self.item_name}", 1, 2,
                                                       column_span=10)
        self.getWidgetSet().add_button("+", 4, 24, command=self.changevalue("add"), padx=0)
        self.getWidgetSet().add_button("-", 4, 22, command=self.changevalue("sub"), padx=0)
        self.getWidgetSet().add_button("Back", 17, 0, column_span=2, command=self.getManagerPage().changeprevious)

        # Overrides
        self.price._override = True
        self.cat_label._override = True
        self.final_price._override = True

        # Color
        self.label.set_color(py_tui.colors.get_colour_pair(random.randrange(100, 250), -1))
        self.label.set_border_color(57)
        self.cart_qty.set_color(py_tui.colors.get_colour_pair(random.randrange(100, 250), -1))
        self.cart_qty.set_border_color(57)
        self.cat_label.set_color(py_tui.colors.get_colour_pair(random.randrange(100, 250), -1))

        # Text Block
        text_block.set_text(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{'404 Image Not Found':^68}")

        self.useItem(ItemView({
            'item_name': 'Cereal',
            'item_price': 7,
            'item_catagory': 'packaged_goods',
            'id': '3828500589576'
        }))

    def changevalue(self, operation):
        def run():
            if operation == "add":
                self.qty += 1
            elif operation == "sub":
                if self.qty != 0:
                    self.qty -= 1
            self.total = self.item_price * self.qty
            self.cart_qty.set_title(str(self.qty))
            self.final_price.set_title(f"Total Price:S${self.total:.2f}")

        return lambda: run()

    def useItem(self, itemview: ItemView, update: bool = False):
        if update:
            self.add_cart.set_title("Update Cart")
        self.item_view = itemview
        self.qty = itemview.get_qty()
        self.item_price = self.item_view.getGSTPrice()
        self.item_name = self.item_view.getName()
        self.item_catagory = self.item_view.getCatagory()
        self.item_id = self.item_view.item_id

    def add_to_cart(self):
        if self.cart_state.ItemeExists(self.item_id):
            self.cart_state.changeItem(self.item_id, self.qty)
        else:
            self.cart_state.addItem(self.item_id, self.qty)

    def page_refresh(self):
        self.nav_bar.search_bar.set_text(self.getGlobalStates().getNavBarState().getSearch())

    def draw_refresh(self):
        self.label.set_title(f"{self.item_name}")
        self.cart_qty.set_title(str(self.qty))
        self.price.set_title(f"Price: S${float(self.item_price):.2f}")
        self.final_price.set_title(f"Total Price:S${self.total:.2f}")
        self.cat_label.set_title(f"Home / {self.item_catagory} / {self.item_name}", )
        self.getGlobalStates().getNavBarState().UpdateSearch(self.nav_bar.search_bar.get())


class Home(Page):

    def __init__(self, root):
        super().__init__(root, "Home")

    def init_page(self):
        super().init_page()
        self.test_widget()

    def test_widget(self):
        for x in range(18):
            for y in range(17):
                self.getWidgetSet().add_button(f"Test{x * 2},{1 + y}", 1 + y, 0 + (x * 2), column_span=2,padx=0, command=self.changevalue(f"Test{x * 2},{1 + y}"))

    def changevalue(self, value):
        def run():
            self.nav_bar.current_cell.set_title(value)

        return lambda: run()

    def page_refresh(self):
        self.nav_bar.search_bar.set_text(self.getGlobalStates().getNavBarState().getSearch())

    def draw_refresh(self):
        self.getGlobalStates().getNavBarState().UpdateSearch(self.nav_bar.search_bar.get())


class Search(Page):
    _catagory_dict = {
        "None": None,
        "Dairy": "dairy",
        "Packaged Goods": "packaged_goods",
        "Canned Goods": "canned_goods",
        "Condiments & Sauces": "condiments_sauces",
        "Drinks & Beverages": "drink_beverages"
    }

    def __init__(self, root):
        super().__init__(root, "Search")
        self.search_state = self.getGlobalStates().getSearchState()
        self.callback = self.update_search

    def init_page(self):
        super().init_page()
        self.search_view: ScrollMenu = self.getWidgetSet().add_custom_widget(ScrollMenu, "Search Result", 2, 7,row_span=14,column_span=11, padx=1, pady=0)
        self.search_view.add_text_color_rule("@.*@", py_tui.get_colour_pair(196, -1), 'contains', match_type='regex')
        self.search_view.add_text_color_rule(";.*;", py_tui.get_colour_pair(11, -1), 'contains', match_type='regex')
        self.search_view.add_text_color_rule("%.*%", py_tui.get_colour_pair(46, -1), 'contains', match_type='regex')
        self.getWidgetSet().add_label("Search Filters", 2, 2, column_span=3)
        self.cat_menu: CheckBoxMenu = self.getWidgetSet().add_custom_widget(CheckBoxMenu, "Catagory", 3, 1, row_span=2, column_span=6, padx=1, pady=0, checked_char="X")
        self.cat_menu.add_item_list(
            ["None", "Dairy", "Packaged Goods", "Canned Goods", "Condiments & Sauces", "Drinks & Beverages"])
        self.cat_menu.mark_item_as_checked("None")
        self.name_sort_button: Button = self.getWidgetSet().add_button("Sorting Name in Asc Order", 6, 1, column_span=6, command=self.change_value("name"))
        self.price_sort_button: Button  = self.getWidgetSet().add_button("Sorting Price in Asc Order", 8, 1, column_span=6, command=self.change_value("price"))
        self.search_view.add_key_command(KEY_ENTER, self.view_item)
        self.nav_bar.search_cell.command = self.update_search

    def update_search(self):
        self.search_state.changeparam("search_name", self.nav_bar.search_bar.get())
        self.search_view.clear()
        for pos, item_view in enumerate(self.search_state.search()):
            item_inv = item_view.getInventory()
            if item_inv > 10:
                item_inv = "%In Stock%"
            elif 0 < item_inv < 10:
                item_inv = ";In Stock;"
            else:
                item_inv = "@Out of Stock@"
            item_price = f"Price: S${item_view.getGSTPrice():.2f}"
            self.search_view.add_item(
                f"{pos + 1:02d}. {item_view.getName():<30} Item {item_view.item_id:<13s} {item_price:<15}       {'' * 35}{item_inv}")

    def view_item(self):
        item_view = self.search_view.get()
        if item_view is not None:
            item_view = self.search_state.getItemView(item_view[40:40+13])
            self.getManagerPage().get_page("page_itemView").useItem(item_view)
            self.getManagerPage().change_page("page_itemView")

    def change_value(self, detail_type):
        def run():
            if detail_type == "name":
                if self.search_state.name_sort:
                    self.name_sort_button.set_title("Sorting Name in Desc Order")
                    self.search_state.changeparam("name_sort", False)
                else:
                    self.name_sort_button.set_title("Sorting Name in Asc Order")
                    self.search_state.changeparam("name_sort", True)
            if detail_type == "price":
                if self.search_state.price_sort:
                    self.price_sort_button.set_title("Sorting Price in Desc Order")
                    self.search_state.changeparam("price_sort", False)
                else:
                    self.price_sort_button.set_title("Sorting Price in Asc Order")
                    self.search_state.changeparam("price_sort", True)
        return lambda: run()

    def page_refresh(self):
        self.nav_bar.search_bar.set_text(self.getGlobalStates().getNavBarState().getSearch())

    def draw_refresh(self):
        cat = self._catagory_dict[self.cat_menu.get_checked_item()]
        self.search_state.changeparam("catagory", cat)
        self.getGlobalStates().getNavBarState().UpdateSearch(self.nav_bar.search_bar.get())


class ShoppingCart(Page):
    def __init__(self, root):
        super().__init__(root, "Shopping Cart")
        self.cart_state: CartState = self.getGlobalStates().getCartState()
        self.callback = self.refresh_cart

    def init_page(self):
        super().init_page()
        self.cart_view: ScrollMenu = self.getWidgetSet().add_custom_widget(ScrollMenu, "Item Cart", 2, 8, row_span=14, column_span=11, padx=1, pady=0)
        self.subtotal_label = self.getWidgetSet().add_label("", 9, 21, column_span=5)
        self.ship_label = self.getWidgetSet().add_label("", 10, 20, column_span=5)
        self.getWidgetSet().add_label(f"  ----------------------------------------", 11,20, column_span=6)
        self.getWidgetSet().add_label(f"  Additional fee(s) be added at checkout  ", 12,20, column_span=6)
        self.est_total = self.getWidgetSet().add_label("",13,20, column_span=6)
        self.est_total._override = True
        self.getWidgetSet().add_button(f"Proceed to Checkout", 15,21, column_span=6, command=self.gotocheckout)
        self.getWidgetSet().add_button("Back", 17, 0, column_span=2, command=self.getManagerPage().changeprevious)
        self.cart_view.add_key_command(KEY_ENTER, self.view_item)
        self.nav_bar.cart_cell.command = self.refresh_cart

    def gotocheckout(self):
        self.getManagerPage().change_page("page_checkout")

    def refresh_cart(self):
        self.cart_view.clear()
        if not self.cart_state.isEmpty():
            for line in self.cart_state.enumerateCart():
                self.cart_view.add_item(line)

    def view_item(self):
        item_view = self.cart_view.get()
        if item_view is not None:
            item_view = self.cart_state.getItemView(item_view[40:40+13])
            self.getManagerPage().get_page("page_itemView").useItem(item_view, update=True)
            self.getManagerPage().change_page("page_itemView")

    def page_refresh(self):
        self.nav_bar.search_bar.set_text(self.getGlobalStates().getNavBarState().getSearch())

    def draw_refresh(self):
        subtotal, ship = self.cart_state.getCartTotal(), 5 if not self.cart_state.isEmpty() else 0
        total = round((self.cart_state.getCartTotalwoGST()+ship)*1.07,2)
        self.subtotal_label.set_title(f"Subtotal: S${subtotal:.2f}")
        self.ship_label.set_title(f"   Shipping & Handling: S${ship:.2f}")
        self.est_total.set_title(f"  Estimated total: S${total:.2f}")
        self.getGlobalStates().getNavBarState().UpdateSearch(self.nav_bar.search_bar.get())


class Profile(Page):
    def __init__(self, root):
        super().__init__(root, "Profile")
        self.profile: UserProfile = None

    def init_page(self):
        super().init_page()
        self.profile_label = self.getWidgetSet().add_label("--Profile--", 1, 16, column_span=2)
        self._create_details("profile_name", f"{'Account Name':>17}", 2)
        self._create_details("profile_dob", f"{'Date Of Birth':>17}", 3)
        self._create_details("profile_phone_num", f"{'Phone Number':>17}", 4)
        self._create_details("profile_email", f"{'Email Address':>17}", 5)
        self.profile_address_label = self.getWidgetSet().add_label(f"{'Address:':>18}", 6, 2, column_span=3)
        self.profile_address = self.getWidgetSet().add_block_label("", 6, 5, row_span=3, column_span=5)
        self.profile_address._override = True
        self.profile_address_button = self.getWidgetSet().add_button("Change", 6, 10, column_span=2)
        self.payment_label = self.getWidgetSet().add_label("--Payment--", 9, 16, column_span=2)
        self.payment_card_label = self.getWidgetSet().add_label(f"{'Payment Method:':>18}", 10, 2, column_span=3)
        self.payment_card = self.getWidgetSet().add_block_label("", 10, 5, row_span=3, column_span=5)
        self.getWidgetSet().add_button("Back", 17, 0, column_span=2,command=self.getManagerPage().changeprevious)
        self.payment_card.set_color(
            py_tui.colors.get_colour_pair(random.Random().randrange(50, 100) - random.Random().randrange(25, 50), -1))
        self.profile_address.set_color(
            py_tui.colors.get_colour_pair(random.Random().randrange(50, 100) - random.Random().randrange(25, 50), -1))
        self.payment_card._override = True
        self.set_details(self.getGlobalStates().getUserProfile())

    def _create_details(self, detail_type, display_name, y):
        setattr(self, f"{detail_type}_label", self.getWidgetSet().add_label(f"{display_name}:", y, 2, column_span=3))
        setattr(self, f"{detail_type}", self.getWidgetSet().add_label("", y, 5, column_span=5))
        getattr(self, f"{detail_type}")._override = True
        fg = random.Random().randrange(100, 255) - random.Random().randrange(25, 50)
        getattr(self, f"{detail_type}").set_color(py_tui.colors.get_colour_pair(fg, -1))
        setattr(self, f"{detail_type}_button", self.getWidgetSet().add_button("Change", y, 10, column_span=2,
                                                                              command=self.show_change_popups(
                                                                                  detail_type)))

    def set_details(self, set_profile: UserProfile):
        self.profile = set_profile

    def change_detail(self, detail_type, newvalue):
        if detail_type == "profile_name":
            detail_type = "name"
        elif detail_type == "profile_dob":
            detail_type = "dateofbirth"
        elif detail_type == "profile_phone_num":
            detail_type = "contact"
        elif detail_type == "profile_email":
            detail_type = "email"
        else:
            detail_type = ""

        self.profile.setdetail(detail_type, newvalue)

    def show_change_popups(self, detail_type):
        def execute():
            def run(new_value):
                self.change_detail(detail_type, new_value)

            self._root.display.show_text_box_popup("Change Value", command=run)

        return lambda: execute()

    def page_refresh(self):
        self.nav_bar.search_bar.set_text(self.getGlobalStates().getNavBarState().getSearch())

    def draw_refresh(self):
        if self.profile is None:
            raise ValueError("Why?")
        self.profile_name.set_title(self.profile.getName())
        self.profile_dob.set_title(datetime.date(*self.profile.getDOB()).strftime("%d %B %Y"))
        self.profile_phone_num.set_title(self.profile.getContact())
        self.profile_email.set_title(self.profile.getEmail())
        self.profile_address.set_title(self.profile.getAddress())
        self.payment_card.set_title(str(self.profile.getPayment()))
        self.getGlobalStates().getNavBarState().UpdateSearch(self.nav_bar.search_bar.get())


class Checkout(Page):
    def __init__(self, root):
        super().__init__(root, "Checkout")
        self.items_cart = self.getGlobalStates().getCartState().cart_items
        self.cart_state = self.getGlobalStates().getCartState()
        self.sales_database = self.getGlobalStates().getSalesDataBase()
        self.discount: bool = False
        self.callback = self.prepareCheckOut
        self.sales_insert = SalesInsertion()

    def init_page(self):
        self.getWidgetSet().add_label(" 1. Shipping Information", 1, 2, column_span=4)
        self.getWidgetSet().add_label("Delivery Address:", 2,3, column_span=3)
        self.profile_address = self.getWidgetSet().add_block_label("", 2, 6, row_span=3, column_span=5)
        self.profile_address._override = True
        self.getWidgetSet().add_label(" 2. Billing Information", 4, 2, column_span=4)
        self.payment_method = self.getWidgetSet().add_block_label("", 5, 3, row_span=3, column_span=5)
        self.payment_method._override = True
        self.getWidgetSet().add_label(" 3. Review Items and Shipping", 7,2, column_span=4)
        self.cart_view: ScrollMenu = self.getWidgetSet().add_custom_widget(ScrollMenu, "Item Cart", 8, 2, row_span=10, column_span=11, padx=1, pady=0)
        self.getWidgetSet().add_label("Order Summary", 1, 18, column_span=3)._override = True
        self.getWidgetSet().add_label("Items:", 2, 18, column_span=2)._override = True
        self.getWidgetSet().add_label("Shipping & Handling:", 3, 18, column_span=4)._override = True
        self.items_cost = self.getWidgetSet().add_label("", 2, 22, column_span=2)
        self.items_cost._override = True
        self.shipping_cost = self.getWidgetSet().add_label("", 3, 22, column_span=2)
        self.items_cost._override = True
        self.getWidgetSet().add_label("-"*44, 4, 18, column_span=7)._override = True
        self.getWidgetSet().add_label("Total Before Tax:", 5,18, column_span=3)._override = True
        self.total_btax_cost = self.getWidgetSet().add_label("", 5, 22, column_span=2)
        self.getWidgetSet().add_label("Estimated Tax:", 6, 18, column_span=3)._override = True
        self.tax_cost = self.getWidgetSet().add_label("", 6, 22, column_span=2)
        self.getWidgetSet().add_label("Net Payable:", 7, 18, column_span=3)._override = True
        self.net_payable = self.getWidgetSet().add_label("", 7, 22, column_span=2)
        self.getWidgetSet().add_label("-" * 44, 8, 18, column_span=7)._override = True
        self.getWidgetSet().add_button("Place Order", 9, 18, column_span=7, command=self.placeOrder)
        self.getWidgetSet().add_label("Enter Discount Card Number", 14, 18, column_span=4)
        self.discount_bar = self.getWidgetSet().add_text_box("",15,18,column_span=12)
        self.dicount_button = self.getWidgetSet().add_button("Verify", 15, 30, column_span=3, command=self.verifyCard)

    def verifyCard(self):
        text = self.discount_bar.get().replace("-", "")
        if text in database.Constants.discount_card_nums:
            self.dicount_button.set_title("Verified")
            self.discount = True
        else:
            self.dicount_button.set_title("Verify")
            self.discount = False

    def prepareCheckOut(self):
        self.profile_address.set_title(self.getGlobalStates().getUserProfile().getAddress())
        self.payment_method.set_title(str(self.getGlobalStates().getUserProfile().getPayment()))
        cart_total = self.cart_state.getCartTotalwoGST()
        subtotal, ship_cost = f"S${cart_total*1.07:.2f}", f"S${5:.2f}"
        self.items_cost.set_title(f"{subtotal:<18s}")
        self.shipping_cost.set_title(f"{ship_cost:<18s}")
        cart_total = cart_total * 0.9 if self.discount else cart_total
        cart_total += 5
        btotal, tax = f"S${cart_total:.2f}", f"S${cart_total*0.07:.2f}"
        net_pay = f"S${cart_total*1.07:.2f}"
        self.total_btax_cost.set_title(f"{btotal:<18s}")
        self.tax_cost.set_title(f"{tax:<18s}")
        self.net_payable.set_title(f"{net_pay:<18s}")
        self.refresh_cart()

    def refresh_cart(self):
        self.cart_view.clear()
        if not self.cart_state.isEmpty():
            for line in self.cart_state.enumerateCart():
                self.cart_view.add_item(line)

    def placeOrder(self):
        total = self.cart_state.getCartTotalwoGST()
        discount_given = round(total * 0.1 if self.discount else 0,2)
        cart_total = round((total * 0.9 if self.discount else total),2)
        order_num = database.generate_EAN13()
        self.sales_insert.setOrderNumber(order_num)
        with open(f"./receipts/receipt {datetime.datetime.now()}.txt", "w+") as f:
            f.write(f"Bill {order_num}\n")
            f.write(f"--Items{'-'*78}\n")
            for line in self.cart_state.genrecipt():
                f.writelines(line)
            f.write("\n")
            f.write(f"{'-'*85}\n")
            f.write(f"           Subtotal: S${round(cart_total*1.07,2):.2f}\n")
            f.write(f"           Discount: S${discount_given:.2f}\n")
            cart_total += 5
            btotal, tax = cart_total, round(cart_total * 0.07,2)
            f.write(f"Shipping & Handling: S$5.00\n")
            f.write(f"   Total before Tax: S${btotal:.2f}\n")
            f.write(f"                Tax: S${tax:.2f}\n")
            f.write(f"              Total: S${round(cart_total*1.07,2):.2f}")
            self.sales_insert.set_payable(round(cart_total*1.07,2))
            self.sales_insert.setRoundings(self.cart_state, self.discount)
        self.getManagerScreen().display.show_message_popup("Info", "Order Placed", color=py_tui.DEFAULT_COLOR)
        self.sales_insert.setTimeStamp()
        self.sales_database.add_customer_sale(self.sales_insert.gen_insert())
        self.cart_state.clearCart()
        self.getManagerScreen().display.apply_widget_set(self.getManagerPage().get_page("page_home").getWidgetSet())

    def page_refresh(self):
        pass

    def draw_refresh(self):
        text = self.discount_bar.get().replace("-", "")
        self.discount_bar.set_text('-'.join(text[i:i+5] for i in range(0, len(text), 5)))
        self.discount_bar._move_right()
        self.sales_insert.set_cart(self.cart_state)
        self.sales_insert.set_discount(text)
        self.sales_insert.set_customer_id(self.getGlobalStates().getUserProfile().getUUID())
        self.prepareCheckOut()