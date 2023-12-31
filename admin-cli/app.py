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

import getpass as secureinput
import os

import authenication
import cli2
import logger
from pyfiglet import Figlet

logger.initdebuglogger()

login = None
debug = True  # DEBUG FLAG

while login is not True and debug is False:
    os.system("clear")
    print(Figlet(font='slant').renderText('NTUC Terminal'))
    print("Please enter your Username and Password")

    login = authenication.authenicate((str(input("Username: "))), (secureinput.getpass("Password: ")))

os.system("clear")
print("Welcome Back, DariusSG")
terminal = cli2.Interpreter(intro="Type help or ? to list commands.\n", prompt="[admin]>>> ")
terminal._addmodulesfromdirectory('./script')
terminal.cmdloop()