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
from typing import Optional

from states.classItem import ItemView
from database import main_Database, item_Table


class SearchView:
    def __init__(self, item_database: main_Database):
        self.database: item_Table = item_database.get_item_database()
        self.search_name: str = ""
        self.catagory: Optional[str] = None
        self.name_sort: bool = True
        self.price_sort: bool = True
        self.result = []
        self.hash = 0

    def _get_hash(self):
        return hash("".join(list(map(str, [self.search_name, self.catagory, self.name_sort, self.price_sort]))))

    def search(self):
        if self.hash != int(self._get_hash()):
            self.hash, self.result = int(self._get_hash()), self.database.search(self.search_name, self.catagory, self.price_sort, self.name_sort)
        return self.result

    def getItemView(self, item_id):
        return ItemView(self.database.getItembyID(item_id))

    def changeparam(self, param_type, value):
        if param_type not in ["search_name", "catagory", "name_sort", "price_sort"]:
            return False
        else:
            setattr(self, param_type, value)