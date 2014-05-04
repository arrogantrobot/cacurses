#!/usr/bin/env python

import curses
from cursebuf import cursebuf
from ca import ca
from infobox import infobox
import time

class ca_app:
    def __init__(self): 
        self.wait_time = 0.05
        self.main()

    def start(self):
        self.brush_start = 33
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        (self.max_y,self.max_x) = self.stdscr.getmaxyx()
        self.cb = cursebuf(self.max_y-1)
        self.ca = ca(self.max_x)
        self.info_win = infobox(30, 4, 0, 0)
        curses.start_color()
        curses.noecho()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)

    def stop(self):
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()
        exit()

    def update(self):
        s = "".join( map( self.brush, self.ca.get_next() ) )
        self.cb.add_line(s)
        self.draw()

    def draw(self):
        for (y, line) in enumerate(self.cb.get_buf()):
            v = buffer(line)
            for n in range(len(line)):
                attr = 2 if v[n] == " " else 1
                self.stdscr.addstr(int(y),int(n),v[n], curses.color_pair(attr))
        self.stdscr.move(0,0)
    def brush(self, v):
        return self.brush_set[v]

    def act(self, c):
        if c == curses.KEY_LEFT:
            self.ca.decrement_rule()
        elif c == curses.KEY_RIGHT:
            self.ca.increment_rule()
        elif c == ord('r'):
            self.ca.reset()
        elif c == ord(' '):
            self.pause = not self.pause
        elif c == curses.KEY_UP:
            self.wait_time -= self.wait_time * 0.10
        elif c == curses.KEY_DOWN:
            self.wait_time += self.wait_time * 0.10
        elif c == 27 or c == ord('q'):
            self.stop()
        if not self.pause:
            self.update()
            self.stdscr.refresh()
            self.info_win.update(self.ca.get_rule(), 1 / self.wait_time)

    def main(self):
        self.start()
        b = "X"
        self.brush_set = { 0: " ", 1: b }
        try:
            self.stdscr.nodelay(1)
            self.pause = False
            while True:
                c = self.stdscr.getch()
                self.act(c)
                time.sleep(self.wait_time)
            time.sleep(1)
        finally:
            self.stop()

if __name__ == "__main__":
    ca = ca_app()
