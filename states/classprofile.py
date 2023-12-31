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

from random import randrange
from uuid import uuid4


class Payment:
    vaild_cardtype = ["Visa", "Mastercard"]

    def __init__(self, cardname, cardtype, card_num, exp_date, cvv_code):
        self.card_name = cardname
        if cardtype not in self.vaild_cardtype:
            raise Exception("Invalid Card Type")
        self._cardtype = cardtype

        self._card_num: str = card_num
        if self._validate_card() is False:
            raise Exception("Invaild Card Number")

        if (not cvv_code.isdigit()) or exp_date == "":
            raise Exception("Invaild card CVV or Expiry Date")
        self._cvv_code, self.exp_date = cvv_code, exp_date

    def _validate_card(self):
        """
        Input: Card number, integer or string
        Output: Valid?, boolean
        """
        double, total = 0,0
        digits = self._card_num.replace(" ", "")

        for i in range(len(digits) - 1, -1, -1):
            for c in str((double + 1) * int(digits[i])):
                total += int(c)
            double = (double + 1) % 2

        return (total % 10) == 0

    def processPayment(self, net_payable):
        auth = str(int(net_payable) + int(self._cvv_code) ** 2)[0:3]
        numbers = [randrange(10) for _ in range(12)]
        ref_code, batch_trace = ''.join(map(str, numbers[0:6])), ''.join(map(str, numbers[6:]))
        numbers = [randrange(10) for _ in range(10)]
        auth_code = [int(x) for x in 2 * str(auth)]
        approval = [numbers[(int(ref_code[x]) + auth_code[x]) - int(batch_trace[x])] for x in range(6)]
        return ref_code, batch_trace, approval

    def __str__(self):
        censored = []
        for i in self._card_num[0:-4]:
            if i != " ":
                censored.append("X")
            else:
                censored.append(" ")
        return f" Name: {self.card_name} | Type: {self._cardtype}\n Number: {''.join([*censored, self._card_num[-4:]])}\n Expiry: {self.exp_date}"


class UserProfile:
    def __init__(self):
        self._gen_UUID()
        self._name = None
        self._dateofbirth = None
        self._contact = None
        self._email = None
        self._address = None
        self._payment: Payment = None

    def getUUID(self):
        return self._uuid

    def getName(self):
        return self._name

    def getDOB(self):
        return self._dateofbirth

    def getContact(self):
        return self._contact

    def getEmail(self):
        return self._email

    def getAddress(self):
        return self._address

    def getPayment(self):
        return self._payment

    def _gen_UUID(self):
        self._uuid = uuid4()

    def setdetail(self, detail_type, new_value):
        if detail_type not in ["name", "dateofbirth", "email", "contact", "address", "payment"]:
            return False
        elif detail_type == "payment" and not isinstance(new_value, Payment):
            return False
        else:
            setattr(self, f"_{detail_type}", new_value)
            return True


def gen_test_profile():
    test_profile = UserProfile()
    data = [
        ("name", "Darius Koh"), 
        ("dateofbirth", (2005, 1, 26)), 
        ("email", "sg50koh@gmail.com"), 
        ("contact", "9647 9874"), 
        ("address", " EdgeField Plains\n Blk 669B #18-662\n Singapore 822669"), 
        ("payment", Payment("Darius Koh", "Visa", "5245 3949 4412 9593", "7/27", "369"))
    ]
    for detail_type, new_value in data:
        test_profile.setdetail(detail_type, new_value)
    return test_profile