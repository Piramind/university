import curses
import time
import pygame
import abc

from life import GameOfLife


class UI(abc.ABC):
    def __init__(self, life: GameOfLife):
        self.life = life

    @abc.abstractmethod
    def run(self):
        pass


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)


    def draw_borders(self, screen):
        screen.addstr(0, 0, '+')
        screen.addstr(self.life.rows + 1, 0, '+')
        screen.addstr(0, self.life.cols + 1, '+')
        screen.addstr(self.life.rows + 1, self.life.cols + 1, '+')

        for i in range(1, self.life.cols + 1):
            screen.addstr(0, i, '-')
            screen.addstr(self.life.rows + 1, i, '-')
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.life.cols + 1, '|')


    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, '*')


    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()

        sleep_time = 0.5
        while not self.life.is_max_generations_exceeded:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(sleep_time)
            self.life.step()

        time.sleep(sleep_time)
        screen.clear()
        screen.addstr(0, 0, 'The Game Is Over')
        screen.refresh()
        time.sleep(2)
        curses.endwin()


if __name__ == '__main__':
    life = GameOfLife((24, 24), max_generations=10)
    ui = Console(life)
    ui.run()
