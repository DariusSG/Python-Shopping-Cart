import accounting
from database import generate_EAN13, DatabaseUpdateFailed, main_Database
from datetime import datetime
from rapidtable import format_table, FORMAT_GENERATOR_COLS
from termcolor import colored

_primary = main_Database("/home/dariussg/PycharmProjects/Mini Project/database.etdb", "HeM6Rr784^n@LqdvbYKy!xX75sX4wJgV")
inv_table = _primary.get_item_database()
sales_table = _primary.get_sales_database()


def command_addItem(arguments):
    if len(arguments) != 3:
        return "ERROR"
    if arguments[1] not in inv_table.CATAGORY:
        print("Item Catagory Not Vaild")
    if not arguments[2].replace(".", "").isdigit():
        print("Item Price Not Vaild")
    inv_table.add_item(arguments[0].replace("%", " "), arguments[1], arguments[2], generate_EAN13())
    print("Added Item")
    return True


def command_viewItem(arguments):
    if len(arguments) != 1:
        return "ERROR"
    if not((arguments[0].isdigit()) or (arguments[0] == "all")):
        print("Item ID Not Vaild")
        return "ERROR"
    if arguments[0] == "all":
        lst = inv_table._db.all()
    else:
        lst = [inv_table.getItembyID(arguments[0])]
        if lst == [None]:
            print("Item ID Not Vaild")
            return "ERROR"
    print_table(format_itemview(lst))
    return True


def command_addInventory(arguments):
    if len(arguments) != 2:
        return "ERROR"
    if not arguments[0].isdigit():
        print("Item ID Not Vaild")
    if not arguments[1].isdigit():
        print("Item ID Not Vaild")
    try:
        inv_table.add_inventory(arguments[0], int(arguments[1]))
        print("Added Inventory to Item")
    except DatabaseUpdateFailed as e:
        print(e)
        return "ERROR"
    return True


def command_viewSale(arguments):
    if len(arguments) != 3 and validate(arguments[1]) is None and validate(arguments[2]) is None:
        return "ERROR"
    start, end = datetime.strptime(arguments[1], "%Y-%m-%d"), datetime.strptime(arguments[2], "%Y-%m-%d")
    total_sale, daily_sale = accounting.collect_data(sales_table.getSales(), start, end)
    print("Total Sales")
    print_table2(total_sale)
    print("\n\nDaily Sales")
    for day in daily_sale:
        print(f"Sales for {day}")
        print_table2(daily_sale[day])
    return "ERROR"
# DO NOT MESS UNLESS YOU KNOW WHAT YOU ARE DOING
# {
#     'item_name': 'Milk',
#     'item_price': 2.3,
#     'item_catagory': 'dairy',
#     'item_id': '7026020123126'
# }


def format_itemview(x):
    data = []
    for lst in x:
        dct_data = {
            'Item Name': lst["item_name"],
            'Item ID': lst["id"],
            'Item Catagory': lst["item_catagory"],
            'Item Price': currencyformatting(lst["item_price"]),
            'Remaining Stock': lst["item_qty"]
        }
        data.append(dct_data)
    return data


def print_table(y):
    header, rows = format_table(y, fmt=FORMAT_GENERATOR_COLS)
    spacer = '  '
    print(colored(spacer.join(header), color='blue'))
    print(colored('-' * sum([(len(x) + 2) for x in header]), color='magenta'))
    for r in rows:
        print(colored(r[0], color='white') + spacer, end='')
        print(colored(r[1], color='yellow') + spacer, end='')
        print(colored(r[2], color='cyan') + spacer, end='')
        print(colored(r[3], color='red') + spacer, end='')
        print(colored(r[4], color='green'))


def print_table2(total_sale):
    header, rows = format_table([{"Item ID": item_id, "Qty Sold": total_sale[item_id]} for item_id in total_sale],
                                fmt=FORMAT_GENERATOR_COLS)
    spacer = '  '
    print(colored(spacer.join(header), color='blue'))
    print(colored('-' * sum([(len(x) + 2) for x in header]), color='magenta'))
    for r in rows:
        print(colored(r[0], color='white') + spacer, end='')
        print(colored(r[1], color='cyan'))


def currencyformatting(x):
    return "${:,.2f}".format(float(x))


def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            print("Invaild date YYYY-MM-DD")
            return None
        return True
    except ValueError:
        print("Invaild date YYYY-MM-DD")
        return None