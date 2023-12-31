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

from py_tui.py_tui import PyCUI
from UI.page import Home, Profile, Search, ShoppingCart, itemView, Checkout
from datetime import datetime

from states.classCommon import CommonState


class ManagerScreen:
    def __init__(self):
        self.display = PyCUI(18, 18, auto_focus_buttons=True)
        self.display.enable_logging(f"./logs/{datetime.now()}.log")
        self.display.toggle_unicode_borders()
        self.display.set_refresh_timeout(0.1)
        self.display.set_title("Online Grocery Store")
        self.page_manager = ManagerPage(self)
        self.page_manager.register_page("page_itemView", itemView(self))
        self.page_manager.register_page("page_home", Home(self))
        self.page_manager.register_page("page_profile", Profile(self))
        self.page_manager.register_page("page_search", Search(self))
        self.page_manager.register_page("page_cart", ShoppingCart(self))
        self.page_manager.register_page("page_checkout", Checkout(self))
        self.page_manager.init_page()
        self.page_manager.set_deafult_page("page_home")
        self.display.set_on_draw_update_func(self.page_manager.refresh_page)


    def start(self):
        self.page_manager.change_page("page_home")
        self.display.start()
        self.page_manager.close()


class ManagerPage:
    def __init__(self, screen_manager: ManagerScreen):
        self.screen_manager: ManagerScreen = screen_manager
        self.global_states: CommonState = CommonState()
        self.selected_page: str = ""
        self.previous_page: str = ""
        self.default_page: str  = ""
        self.page_lst: list = []

    def set_deafult_page(self, name: str):
        self.default_page = name

    def register_page(self, name, page):
        self.page_lst.append((name, page))
        setattr(self.screen_manager, str(name), page)

    def get_page(self, name):
        if name == "":
            name = self.default_page
        return getattr(self.screen_manager, str(name))

    def change_page(self, name):
        self.previous_page, self.selected_page = self.selected_page, name
        if self.get_page(name).callback is not None:
            command = self.get_page(name).callback
            command()
        self.screen_manager.display.apply_widget_set(self.get_page(name).getWidgetSet())

    def changeprevious(self):
        self.previous_page, self.selected_page = "", self.previous_page
        self.screen_manager.display.apply_widget_set(self.get_page(self.selected_page).getWidgetSet())

    def init_page(self):
        for _, page in self.page_lst:
            page.init_page()

    def refresh_page(self):
        for name, page in self.page_lst:
            if self.selected_page == name:
                page.draw_refresh()
            page.page_refresh()

    def close(self):
        self.global_states.close()


def run():
    root = ManagerScreen()
    root.start()


run()
