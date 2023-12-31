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

import sys
sys.path.extend(['/home/dariussg/PycharmProjects/Mini Project/'])

from database import main_Database, Constants
# {
#     'item_name': 'Milk',
#     'item_price': 2.3,
#     'item_catagory': 'dairy',
#     'item_id': '7026020123126'
# }
primary_database = main_Database("./database.etdb", "HeM6Rr784^n@LqdvbYKy!xX75sX4wJgV")
item_table = primary_database.get_item_database()
for items in Constants.item_list:
    item_table.add_item(items["item_name"], items["item_catagory"], items["item_price"], items["item_id"])
    item_table.add_inventory(items["item_id"], 1000)

for itemsdict in item_table._db.all():
    print(itemsdict)
primary_database.close()