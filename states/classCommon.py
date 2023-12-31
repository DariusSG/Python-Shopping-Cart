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

import database
from states.classCart import CartState
from states.classNavBar import NavBarState
from states.classSearch import SearchView
from states.classprofile import UserProfile, gen_test_profile
from database import main_Database


class CommonState:
    def __init__(self):
        self._database = main_Database("./database.etdb", "HeM6Rr784^n@LqdvbYKy!xX75sX4wJgV")
        self._profile: UserProfile = gen_test_profile()
        self._cart: CartState = CartState(self._database)
        self._search: SearchView = SearchView(self._database)
        self._nav_bar_state: NavBarState = NavBarState()

    def getSalesDataBase(self):
        return self._database.get_sales_database()

    def getUserProfile(self):
        return self._profile

    def getCartState(self):
        return self._cart

    def getSearchState(self):
        return self._search

    def getNavBarState(self):
        return self._nav_bar_state

    def close(self):
        self._database.close()
