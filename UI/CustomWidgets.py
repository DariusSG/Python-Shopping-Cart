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

import itertools
from wcwidth import wcwidth
from typing import Any, Generator, Iterator, Tuple

from py_tui.ui import MenuImplementation, TextBoxImplementation
from py_tui.widgets import Widget
from py_tui.keys import KEY_UP_ARROW, KEY_DOWN_ARROW, KEY_HOME, KEY_END, KEY_PAGE_UP, KEY_PAGE_DOWN, \
    LEFT_MOUSE_DBL_CLICK, LEFT_MOUSE_CLICK, KEY_ENTER, KEY_DELETE, KEY_BACKSPACE, KEY_RIGHT_ARROW, KEY_LEFT_ARROW



def pad_actual_length(source: Iterator[str], pad: str = "\u200b") -> Tuple[str, Generator[str, None, None]]:
    """
    Determine real-displaying character length, and provide padding accordingly to match length.
    This way slicing will cut asian letters properly, not breaking tidy layouts.
    Don't expect to have 0-width characters in given string!
    :param source: Original string to be manipulated. Accepts Iterator[str], allowing lazy generator.
    :param pad: Default character to pad, default ZWSP
    :return: padding character and lazy generator for padded string
    """

    def inner_gen(source_: Iterator[str]) -> Generator[str, None, None]:
        for char in source_:
            yield char
            if wcwidth(char) == 2:
                yield pad

    return pad, inner_gen(source)
    # https://github.com/microsoft/terminal/issues/1472
    # Windows Terminal + (Powershell/CMD) combo can't run this due to ZWSP width issue.
    # Expected to run in purely CMD / Linux Terminal. or WSL + Windows Terminal.
    # Tested on Xfce4 & CMD.


def fit_to_actual_width_multiline(text: str, length_lim: int) -> Generator[Tuple[int, str], None, None]:
    """
    Cuts given text with varying character width to fit inside given width.
    Will yield multiple lines if line length exceed given length_lim.
    :param text: Source text
    :param length_lim: length limit in 1-width characters
    :return: lazy generator yielding multi-line cut strings
    """

    _, padded = pad_actual_length(text)

    def generator():
        next_line = ''
        line_size = length_lim

        # while line := "".join(itertools.islice(padded, 0, line_size)):

        pos = 0
        while True:
            line = "".join(itertools.islice(padded, 0, line_size))
            if not line:
                break

            # Add contents of next_line, then reset line length if next_line is not empty
            if next_line:
                line = next_line + line
                next_line = ''
                line_size = length_lim

            # check if last text was 2-width character. If so, move it to next_line and adjust next line_size.
            if wcwidth(line[-1]) == 2:
                next_line = line[-1]
                line = line[:-1]
                line_size -= 1

            yield pos, line
            pos += 1

    return generator()


class ScrollMenu(Widget, MenuImplementation):
    """A scroll menu widget.
    """

    def __init__(self, id, title: str, grid: 'py_tui.grid.Grid', row: int, column: int, row_span: int, column_span: int,
                 padx: int, pady: int, logger: 'py_tui.debug.PyCUILogger'):
        """Initializer for scroll menu. calls superclass initializers and sets help text
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        MenuImplementation.__init__(self, logger)
        self.set_help_text('Focus mode on ScrollMenu. Use Up/Down/PgUp/PgDown/Home/End to scroll, Esc to exit.')
        self.get_border_after_draw()

    def _scroll_up(self) -> None:
        """Function that scrolls the view up in the scroll menu
        """

        if 0 < self._top_view == self._selected_item:
            self._top_view = self._top_view - 1
        if self._selected_item > 0:
            self._selected_item = self._selected_item - 1

        self._logger.debug(f'Scrolling up to item {self._selected_item}')

    def _scroll_down(self, viewport_height: int) -> None:
        """Function that scrolls the view down in the scroll menu

        TODO: Viewport height should be calculated internally, and not rely on a parameter.

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """

        if self._selected_item < len(self._view_items) - 1:
            self._selected_item = self._selected_item + 1
        if self._selected_item > self._top_view + viewport_height:
            self._top_view = self._top_view + 1

        self._logger.debug(f'Scrolling down to item {self._selected_item}')

    def _handle_mouse_press(self, x: int, y: int, mouse_event: int):
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        # For either click or double click we want to jump to the clicked-on item
        if mouse_event == LEFT_MOUSE_CLICK or mouse_event == LEFT_MOUSE_DBL_CLICK:
            current = self.get_selected_item_index()
            viewport_top = self._start_y + self._pady + 1

            if viewport_top <= y <= viewport_top + len(self._view_items) - self._top_view:
                elem_clicked = y - viewport_top + self._top_view
                self.set_selected_item_index(elem_clicked)

            if self.get_selected_item_index() != current and self._on_selection_change is not None:
                self._process_selection_change_event()

        # For scroll menu, handle custom mouse press after initial event, since we will likely want to
        # have access to the newly selected item
        Widget._handle_mouse_press(self, x, y, mouse_event)

    def _handle_key_press(self, key_pressed: int) -> None:
        """Override base class function.

        UP_ARROW scrolls up, DOWN_ARROW scrolls down.

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """

        Widget._handle_key_press(self, key_pressed)

        current = self.get_selected_item_index()
        viewport_height = self.get_viewport_height()//2

        if key_pressed == KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == KEY_DOWN_ARROW:
            self._scroll_down(viewport_height)
        if key_pressed == KEY_HOME:
            self._jump_to_top()
        if key_pressed == KEY_END:
            self._jump_to_bottom(viewport_height)
        if key_pressed == KEY_PAGE_UP:
            self._jump_up()
        if key_pressed == KEY_PAGE_DOWN:
            self._jump_down(viewport_height)
        if self.get_selected_item_index() != current and self._on_selection_change is not None:
            self._process_selection_change_event()

    def get_border_after_draw(self):
        height, width = self.get_absolute_dimensions()
        self._border_x_start, self._border_y_start = self._start_x + self._padx, self._start_y + self._pady
        self._border_height, self._border_width = (height - self._pady - 1), (width - 2 * self._padx)

    def _draw(self) -> None:
        """Overrides base class draw function
        """

        Widget._draw(self)
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        offset = -1
        abs_y, abs_x = self.get_absolute_dimensions()
        usable_x = abs_x - 6
        for item in self._view_items:
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                for pos, line in fit_to_actual_width_multiline(str(item), usable_x + offset):
                    if line_counter == self._selected_item:
                        self._renderer.draw_text(self, line, self._start_y + counter + pos, selected=True)
                    else:
                        self._renderer.draw_text(self, line, self._start_y + counter + pos)
                counter = counter + 2
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)


class CheckBoxMenuImplementation(MenuImplementation):
    """Class representing checkbox menu ui implementation

    Attributes
    ----------
    _selected_item_dict : dict of object -> bool
        stores each object and maps to its current selected status
    _checked_char : char
        Character to mark checked items
    """

    def __init__(self, logger, checked_char):
        """Initializer for the checkbox menu implementation
        """

        super().__init__(logger)
        self._selected_item_check = None
        self._checked_char = checked_char

    def get_checked_item(self) -> str:
        return self._selected_item_check

    def toggle_item_checked(self, item: Any):
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Toggle item checked state
        """
        if self._selected_item_check is not None:
            if self._selected_item_check != item:
                self._selected_item_check = item
            else:
                self._selected_item_check = None
        else:
            self._selected_item_check = item

    def mark_item_as_checked(self, item: Any) -> None:
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Toggle item checked state
        """

        self._selected_item_check = item

    def mark_item_as_not_checked(self, item) -> None:
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Item to uncheck
        """

        self._selected_item_check = None


class CheckBoxMenu(Widget, CheckBoxMenuImplementation):
    """Extension of ScrollMenu that allows for multiple items to be selected at once.

    Attributes
    ----------
    selected_item_list : list of str
        List of checked items
    checked_char : char
        Character to represent a checked item
    """

    def __init__(self, id, title: str, grid: 'py_tui.grid.Grid', row: int, column: int, row_span: int, column_span: int,
                 padx: int, pady: int, logger, checked_char: str):
        """Initializer for CheckBoxMenu Widget
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        CheckBoxMenuImplementation.__init__(self, logger, checked_char)
        self.set_help_text(
            'Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.')
        self.get_border_after_draw()

    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """

        Widget._handle_mouse_press(self, x, y, mouse_event)
        viewport_top = self._start_y + self._pady + 1
        if viewport_top <= y <= viewport_top + len(self._view_items) - self._top_view:
            elem_clicked = y - viewport_top + self._top_view
            self.set_selected_item_index(elem_clicked)
            self.mark_item_as_checked(self._view_items[elem_clicked])

    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of key presses.

        First, run the superclass function, scrolling should still work.
        Adds Enter command to toggle selection

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        Widget._handle_key_press(self, key_pressed)
        viewport_height = self.get_viewport_height()
        if key_pressed == KEY_UP_ARROW:
            self._scroll_up()
        if key_pressed == KEY_DOWN_ARROW:
            self._scroll_down(viewport_height)
        if key_pressed == KEY_HOME:
            self._jump_to_top()
        if key_pressed == KEY_END:
            self._jump_to_bottom(viewport_height)
        if key_pressed == KEY_PAGE_UP:
            self._jump_up()
        if key_pressed == KEY_PAGE_DOWN:
            self._jump_down(viewport_height)
        if key_pressed == KEY_ENTER:
            self.toggle_item_checked(self.get())

    def get_border_after_draw(self):
        height, width = self.get_absolute_dimensions()
        self._border_x_start, self._border_y_start = self._start_x + self._padx, self._start_y + self._pady
        self._border_height, self._border_width = (height - self._pady - 1), (width - 2 * self._padx)

    def _draw(self) -> None:
        """Overrides base class draw function
        """

        Widget._draw(self)
        self._renderer.set_color_mode(self._color)
        self._renderer.draw_border(self)
        counter = self._pady + 1
        line_counter = 0
        for item in self._view_items:
            if self._selected_item_check == item:
                line = f'[{self._checked_char}] - {str(item)}'
            else:
                line = f'[ ] - {str(item)}'
            if line_counter < self._top_view:
                line_counter = line_counter + 1
            else:
                if counter >= self._height - self._pady - 1:
                    break
                if line_counter == self._selected_item:
                    self._renderer.draw_text(self, line, self._start_y + counter, selected=True)
                else:
                    self._renderer.draw_text(self, line, self._start_y + counter)
                counter = counter + 1
                line_counter = line_counter + 1
        self._renderer.unset_color_mode(self._color)
        self._renderer.reset_cursor(self)
