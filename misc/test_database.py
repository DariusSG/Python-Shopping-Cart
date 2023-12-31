import sys
sys.path.append('/home/dariussg/PycharmProjects/Mini Project/')

from database import main_Database, Constants
# {
#     'item_name': 'Milk',
#     'item_price': 2.3,
#     'item_catagory': 'dairy',
#     'item_id': '7026020123126'
# }
primary_database = main_Database("./database.etdb", "HeM6Rr784^n@LqdvbYKy!xX75sX4wJgV")
item_table = primary_database.get_item_database()
key = ""
while key != "exit":
    key = input(": ")
    lst = item_table.search("", key)
    print(lst)
    for i in lst:
        print(str(i.getName()))
primary_database.close()