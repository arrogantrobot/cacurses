#!/usr/bin/env python

import curses
import curses.wrapper
from cursebuf import cursebuf
from ca import ca
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
        curses.start_color()
        curses.noecho()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    def stop(self):
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()

    def update_old(self):
        for y in range(1, self.max_y-1):
            brush = self.get_brush()
            for x in range(1, self.max_x-1):
                self.stdscr.addstr(int(y),int(x), brush)

    def update(self):
        s = "".join( map( self.brush, self.ca.get_next() ) )
        self.cb.add_line(s)
        self.draw()

    def draw(self):
        for (y, line) in enumerate(self.cb.get_buf()):
            v = buffer(line)
            for n in range(len(line)):
                self.stdscr.addch(int(y),int(n),v[n])
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
        if not self.pause:
            self.update()
            self.stdscr.refresh()

    def main(self):
        self.start()
        self.brush_set = { 0: " ", 1: "X"}
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
