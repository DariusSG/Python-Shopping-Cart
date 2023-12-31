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

from abc import ABC, abstractmethod

from py_tui.widget_set import WidgetSet
from py_tui.widgets import Label, Button, TextBox

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen_manager import ManagerScreen


class Page(ABC):
    def __init__(self, root, page_name):
        self._root: ManagerScreen = root
        self.page_name: str = page_name
        self._root_page: WidgetSet = root.display.create_new_widget_set(18, 36)
        self.nav_bar: navigation_bar = None
        self.callback = None

    def getGlobalStates(self):
        return self._root.page_manager.global_states

    def getManagerPage(self):
        return self._root.page_manager

    def getManagerScreen(self):
        return self._root

    def getWidgetSet(self):
        """Return WidgetSet for apply_widget_set"""
        return self._root_page

    @abstractmethod
    def init_page(self):
        """Add widget creation here"""
        self.nav_bar: navigation_bar = navigation_bar(self._root, self)

    @abstractmethod
    def page_refresh(self):
        """refresh page when called"""
        raise NotImplementedError

    @abstractmethod
    def draw_refresh(self):
        """refresh page if selected (apply_widget_set) """
        raise NotImplementedError


class navigation_bar:
    def __init__(self, root, page: Page):
        self._root: ManagerScreen = root
        self._root_page: Page = page
        self._page: WidgetSet = self._root_page.getWidgetSet()
        self.page_name: str = self._root_page.page_name
        self.search_bar: TextBox = self._page.add_text_box("Search Bar", 0, 9, column_span=16)
        self.current_cell: Label = self._page.add_label(self.page_name, 0, 0, column_span=4,pady=1)
        self.home_cell: Button = self._page.add_button("Home", 0, 4, column_span=2, command=self.changePage("page_home"))
        self.search_cell: Button = self._page.add_button("Search", 0, 6, column_span=2, command=self.changePage("page_search"))
        self.cart_cell: Button = self._page.add_button(" Shopping Cart", 0, 26, column_span=4, command=self.changePage("page_cart"))
        self.profile_cell: Button = self._page.add_button(" Profile", 0, 30, column_span=4, command=self.changePage("page_profile"))

    def changePage(self, page: str):
        def run():
            self.search_bar.set_text("")
            self._root.page_manager.change_page(page)
        return lambda: run()
