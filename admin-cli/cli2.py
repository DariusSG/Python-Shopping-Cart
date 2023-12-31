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

import importlib
import os
import string
import sys
import time

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

from logger import logger

__all__ = ["cli2"]

PROMPT = '>>> '
IDENTCHARS = string.ascii_letters + string.digits + '_'
style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


class Interpreter:
    identchars = IDENTCHARS
    ruler = '='
    lastcmd = ''
    doc_leader = ""
    doc_header = "Available Commands (type help <topic> to get documentation for <topic> ):"
    misc_header = "Miscellaneous help topics:"
    nohelp = "*** No help on %s"
    use_rawinput = 1
    modulelst = []
    internalcmdlst = ["help", "exit", "reload", "listmodules", "listvar"]

    def __init__(self, intro=None, prompt=PROMPT, stdin=None, stdout=None):
        """Instantiate a line-oriented interpreter framework.

        The optional arguments stdin and stdout
        specify alternate input and output file objects; if not specified,
        sys.stdin and sys.stdout are used.

        """
        self.prompt = prompt
        self.intro = intro
        if stdin is not None:
            self.stdin = stdin
        else:
            self.stdin = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout
        self.cmdqueue = []

    def cmdloop(self):
        """Execute Main Loop"""
        self.preloop()  # exec preloop

        if self.intro:  # does intro if exist
            self.stdout.write(str(self.intro) + "\n")

        stop = None
        while not stop:
            if self.cmdqueue:
                line = self.cmdqueue.pop(0)
            else:
                line = self.session.prompt(self.prompt)
            line = self.precmd(line)  # process given input
            stop = self.onecmd(line)  # execute input
            stop = self.postcmd(stop, line)  # post-execute process
        self.postloop()  # post-loop process

    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.
        """
        # Parse command to argument
        return self.parseline(line)

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        # add autocommands (does not add private func to autocommands lst)
        self.autocommands = [item[3:] for item in self.get_names() if (item[-5:] != '__pvt') and (item[:3] == 'do_')]
        # create session
        self.session = PromptSession(completer=WordCompleter(self.autocommands, ignore_case=False))

    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to
        return.
        """
        del self.autocommands, self.session  # remove them

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:  # line is blank
            return None, None, line
        elif line[0] == '?':  # case 2: User enter ?
            line = 'help ' + line[1:]
        elif line[0] == '!':  # case 3: User enter !
            if hasattr(self, 'do_shell'):  # if dev implement shell func, run it, otherwise blank
                line = 'shell ' + line[1:]
            else:
                return None, None, line
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars:  # finds command and it's args
            i = i + 1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def onecmd(self, linecommand):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = linecommand
        if not line:
            return self._emptyline()
        if cmd is None:
            return self._default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self._default(line)
        if cmd in self.internalcmdlst:
            return self._getfunc(cmd)(arg)
        else:
            try:
                terminalclass, func = self._getfunc(cmd)
            except AttributeError:
                return self._default(line)
            return func(terminalclass, arg)

    def _emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

    def _default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        self.stdout.write('*** Unknown syntax: %s\n' % line.split(" ")[0])

    def get_names(self):
        """This method used to pull in base class attributes"""
        lst = [*dir(self.__class__)]
        for modulejs in self.modulelst:
            terminalclass = getattr(getattr(modulejs["module"], 'cli_helper'), "Terminal")
            lst += dir(terminalclass)
        return lst

    def _print_topics(self, header, cmds, maxcol):
        if cmds:
            self.stdout.write("%s\n" % str(header))
            if self.ruler:
                self.stdout.write("%s\n" % str(self.ruler * len(header)))
            self.columnize(cmds, maxcol - 1)
            self.stdout.write("\n")

    def columnize(self, lst, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not lst:
            self.stdout.write("<empty>\n")
            return

        nonstrings = [i for i in range(len(lst))
                      if not isinstance(lst[i], str)]
        if nonstrings:
            raise TypeError("list[i] not a string for i in %s"
                            % ", ".join(map(str, nonstrings)))
        size = len(lst)
        if size == 1:
            self.stdout.write('%s\n' % str(lst[0]))
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(lst)):
            ncols = (size + nrows - 1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows * col
                    if i >= size:
                        break
                    x = lst[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(lst)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows * col
                if i >= size:
                    x = ""
                else:
                    x = lst[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.stdout.write("%s\n" % str("  ".join(texts)))

    def _addmodulesfromdirectory(self, directory):
        try:
            directory_contents = os.listdir(directory)

            for item in directory_contents:
                self._addmodule(os.path.join(directory, item), "".join([directory[2:], ".", item]))
        except OSError as e:
            print("Something Happened\nPlease try again :)")
            logger.error("OSErrot, {}".format(e))
        except ImportError as e:
            print("Something Went Wrong while importing modules\nPlease try again :)")
            logger.error("ImportError, {}".format(e))
        except Exception as e:
            print("Oops, my fault\nPlease try again :)")
            logger.error("Exception, {}".format(e))
        finally:
            logger.info("Done importing cli modules")

    def _addmodule(self, pathdir, importdir):
        if os.path.isdir(pathdir):
            importedmodule = importlib.import_module(importdir)
            modulejs = {
                "module": importedmodule,
                "name": importedmodule.__name__,
                "importdir": importdir,
                "pathdir": pathdir
            }
            self.modulelst.append(modulejs)

    def _removemodule(self, modulename):
        if modulename in [x["name"] for x in self.modulelst]:
            self.modulelst.remove(self._getmodulejs(modulename))
            del sys.modules[modulename]
        else:
            raise ModuleNotFoundError

    def _replacemodule(self, modulename):
        module = self._getmodulejs(modulename)
        self._removemodule(modulename)
        self._addmodule(module["pathdir"], module["importdir"])

    def _getmodulejs(self, modulename):
        for i in self.modulelst:
            if i['name'] == modulename:
                return i

    @staticmethod
    def _getmoduledep(modulename):
        unsortedscriptsysmodules = [module for module in sys.modules if (("script" in module) and ("script" != module))]
        sortedlst = []
        for scriptmodules in unsortedscriptsysmodules:
            mod = sys.modules[scriptmodules]
            if not (hasattr(mod, "__path__") and getattr(mod, '__file__', None) is None) and (
                    scriptmodules != "script.{}".format(modulename)):
                sortedlst.append(sys.modules[scriptmodules])
        return sortedlst

    def _reloadmoduledep(self, modulename):
        for dep in self._getmoduledep(modulename):
            try:
                importlib.reload(dep)
            except ModuleNotFoundError as e:
                print(e)

    def _getfunc(self, command):
        if "do_" in command:
            command = command[3:]
        if command in self.internalcmdlst:
            return getattr(self, "_".join(['do', command]))
        else:
            for modulejs in self.modulelst:
                terminalclass = getattr(getattr(modulejs["module"], 'cli_helper'), "Terminal")
                if hasattr(terminalclass, "_".join(['do', command])):
                    return terminalclass, getattr(terminalclass, "_".join(['do', command]))
            raise AttributeError

    def do_help(self, arg):
        """
        List available commands with "help" or detailed help with "help cmd".
        """
        if arg:
            # XXX check arg syntax
            try:
                func = self._getfunc('help_' + arg)
            except AttributeError:
                try:
                    if arg[-5:] == '__pvt':
                        raise AttributeError
                    doc = self._getfunc('do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            cmds_doc = []
            funchelp = {}
            for name in names:
                if name[:5] == 'help_':
                    funchelp[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_' and name[-5:] != '__pvt':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in funchelp:
                        cmds_doc.append(cmd)
                        del funchelp[cmd]
                    elif self._getfunc(name).__doc__:
                        cmds_doc.append(cmd)
            self.stdout.write("%s\n" % str(self.doc_leader))
            self._print_topics(self.doc_header, cmds_doc, 80)
            self._print_topics(self.misc_header, list(funchelp.keys()), 80)

    def do_exit(self, arg):
        """
        Exit
        """
        if arg:
            print(self.prompt + "No arguments please")
        print("Exiting")
        time.sleep(1)
        return True

    def do_reload(self, arg):
        if arg == "":
            print("No Arguments found")
            return
        arg = arg.split()
        if arg[0] == "all":
            localmodulelst = self.modulelst.copy()
            self.modulelst = []
            for i in localmodulelst:
                print("Reloading", ".".join(i["name"].split(".")[1:]))
                importlib.invalidate_caches()
                self._reloadmoduledep(i["name"])
                self._addmodule(i["pathdir"], i["importdir"])
            self.autocommands = [item[3:] for item in self.get_names() if
                                 (item[-5:] != '__pvt') and (item[:3] == 'do_')]
            self.session = PromptSession(completer=WordCompleter(self.autocommands, ignore_case=False))
        else:
            print("Only argument \'all\' is accepted")

    def do_listmodules(self, arg):
        arg = arg.split()
        if arg[0] == "sys":
            for i in sys.modules:
                print(i)
        elif len(arg) != 0:
            print("No Argument Please")
        else:
            print("Listing all imported Modules")
            for i in self.modulelst:
                print(".".join(i["module"].__name__.split(".")[1:]))
