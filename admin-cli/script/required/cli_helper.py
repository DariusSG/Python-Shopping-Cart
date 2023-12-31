import time
from. import core


class Terminal:
    # ---------- Commands ----------
    def do_addItem(self, arg):
        """Add an Item \nUsage: addItem [ItemName] [ItemCatagory] [item_price]"""
        arguments = parse(arg)
        result = core.command_addItem(arguments)
        if result == "ERROR":
            print(
                "Invaild Arguments \nUsage: addItem [ItemName] [ItemCatagory] [item_price]")

    def do_viewItem(self, arg):
        """View an Item \nUsage: viewItem [ItemID/all]"""
        arguments = parse(arg)
        result = core.command_viewItem(arguments)
        if result == "ERROR":
            print("Invaild Arguments \nUsage: viewItem [ItemID/all]")

    def do_addInventory(self, arg):
        """Add Inventory to An Item \nUsage: addInventory [ItemID] [Amount]"""
        arguments = parse(arg)
        result = core.command_addInventory(arguments)
        if result == "ERROR":
            print("Invaild Argument \nUsage: addInventory [ItemID] [Amount]")

    def do_exit(self, arg):
        """Exit"""
        print("Logging out ...")
        time.sleep(2)
        print("Thanking For Banking with us")
        time.sleep(1)
        return True



def parse(arg):
    return arg.split()
