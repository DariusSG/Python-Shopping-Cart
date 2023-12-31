"""Module containing py_tui logging utilities
"""

# Author:    Jakub Wlodek
# Created:   18-Mar-2020

import os
import fastlogging
import inspect
import py_tui
from typing import Any, Optional


def _enable_logging(logger: 'PyCUILogger', replace_log_file: bool = True, filename: str = 'py_tui.log',
                    logging_level=fastlogging.DEBUG):
    # noinspection GrazieInspection
    """Function that creates basic logging configuration for selected logger

        Parameters
        ----------
        logger : PyCUILogger
            Main logger object
        filename : os.Pathlike
            File path for output logfile
        logging_level : logging.LEVEL, optional
            Level of messages to display, by default logging.DEBUG

        Raises
        ------
        PermissionError
            py_tui logs require permission to cwd to operate.
        TypeError
            Only the custom PyCUILogger can be used here.
        """

    # Remove existing log file if necessary
    abs_path = os.path.abspath(filename)
    if replace_log_file and os.path.exists(abs_path):
        os.remove(abs_path)

    # Permission check and check if we are using custom py_tui logger
    if not os.access(os.path.dirname(abs_path), os.W_OK):
        raise PermissionError('You do not have permission to create py_tui.log file.')


    # Create our logging utility objects
    logger.enable_logging(filename=filename, logging_level=logging_level)


# noinspection PyProtectedMember
def _initialize_logger(py_tui_root: 'py_tui.PyCUI', name: Optional[str] = None, custom_logger: bool = True):
    """Function that retrieves an instance of either the default or custom py_tui logger.
    
    Parameters
    ----------
    py_tui_root : py_tui.PyCUI
        reference to the root py_tui window
    name : str, optional
        The name of the logger, by default None
    custom_logger : bool, optional
        Use a custom py_tui logger, by default True
    
    Returns
    -------
    logger : py_tui.debug.PyCUILogger
        A custom logger that allows for live debugging
    """

    # noinspection PyProtectedMember
    logger = PyCUILogger()
    return logger


class PyCUILogger:
    """Custom logger class for py_tui, extends the base logging.Logger Class
    
    Attributes
    ----------
    py_tui_root : py_tui.PyCUI
        The root py_tui program for which the logger runs
    live_debug : bool
        Flag to toggle live debugging messages
    """

    def __init__(self):
        self.logger = fastlogging.LogInit(maxSize=100000, backupCnt=10000,useThreads=True, console=False)

    def enable_logging(self, filename, logging_level):
        self.logger = fastlogging.LogInit(pathName=filename, maxSize=100000, backupCnt=10000, useThreads=True)
        self.logger.setLevel(logging_level)

    def _get_debug_text(self, text: str) -> str:
        """Function that generates full debug text for the log

        Parameters
        ----------
        text : str
            Log message

        Returns
        -------
        msg : str
            Log message with function, file, and line num info
        """
        current_frame = inspect.currentframe()
        if current_frame and current_frame.f_back and current_frame.f_back.f_back is not None:
            func = current_frame.f_back.f_back.f_code
        return f'{text}: Function {func.co_name} in {os.path.basename(func.co_filename)}:{func.co_firstlineno}'

    def info(self, msg: Any, *args, **kwargs) -> None:  # to overcome signature mismatch in error
        """Override of base logger info function to add hooks for live debug mode

        Parameters
        ----------
        msg

        """

        debug_text = self._get_debug_text(msg)
        self.logger.info(debug_text)

    def debug(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger debug function to add hooks for live debug mode

        Parameters
        ----------
        msg

        """

        debug_text = self._get_debug_text(msg)
        self.logger.debug(debug_text)

    def warn(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger warn function to add hooks for live debug mode

        Parameters
        ----------
        msg

        """

        debug_text = self._get_debug_text(msg)
        self.logger.warning(debug_text)

    def error(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger error function to add hooks for live debug mode

        Parameters
        ----------
        msg

        """

        debug_text = self._get_debug_text(msg)
        self.logger.error(debug_text)

    def critical(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger critical function to add hooks for live debug mode

        Parameters
        ----------
        msg

        """

        debug_text = self._get_debug_text(msg)
        self.logger.critical(debug_text)
