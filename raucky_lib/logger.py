"""
Logger facility to use Tqdm progress bar in Raucky CLI
"""


from dataclasses import dataclass, field
from time import sleep
from typing import Union
from click import Command
from tqdm import tqdm


class TqdmFake:
    """
    Fake Tqdm object
    """

    def __init__(self, **kwargs):
        self.i = 0
        self.funcs = kwargs.get("iterable")

    def __call__(self, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        pass

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        func: Union[Command, None] = None
        try:
            func = self.funcs[self.i]
            self.i += 1
        except IndexError as idx_error:
            raise StopIteration from idx_error
        return func

    def update(self):
        """
        Tqdm update function stub
        """

    def display(self, _msg: str, pos: int):
        """
        Tqdm display function stub
        """

    def clear(self):
        """
        Tqdm clear function stub
        """

    def close(self):
        """
        Tqdm close function stub
        """


@dataclass
class Logger:
    """
    Tqdm object wrapper
    """

    pbar: Union[tqdm, TqdmFake]
    step_pos: int = field(default=1)

    def __post_init__(self):
        self.save_cursor()

    @staticmethod
    def save_cursor():
        """
        Save cursor position
        """

        print("\033[s", end="")

    @staticmethod
    def clear_screen_and_restore_cursor():
        """
        Restore cursor position and clear until end of screen
        """

        print("\033[u\033[J", end="")

    def progress(self, msg: str):
        """
        Run the next step of the tqdm object and
        log the message if necessary
        """

        self.pbar.update()
        self.pbar.display(msg, pos=self.step_pos)
        self.step_pos += 1
        if isinstance(self.pbar, tqdm):
            sleep(0.50)

    def close(self):
        """
        Close properly the progress bar
        """

        self.pbar.clear()
        self.pbar.close()
        self.clear_screen_and_restore_cursor()
