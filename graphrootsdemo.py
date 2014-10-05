#!/usr/bin/env python

import sys
import curses
from cursebuf import cursebuf
from ca import ca
from infobox import infobox
from textnozzle import TextNozzle
import time
import random

rule_min = 15
rule_max = 50

class ca_app:
    def __init__(self, filename): 
        self.wait_time = 0.05
        self.rules = [30, 57, 18, 90, 129, 130, 131, 132, 133]
        self.nozzle = TextNozzle(filename)
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
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def stop(self):
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()
        exit()

    def update(self):
        s = "".join( map( self.textBrush, self.ca.get_next() ) )
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

    def textBrush(self, v):
        return self.nozzle.get_char(v)

    def random_rule(self):
        self.ca.set_rule(random.choice(self.rules))

    def act(self, c):
        if c == curses.KEY_LEFT:
            self.ca.decrement_rule()
        elif c == curses.KEY_RIGHT:
            self.ca.increment_rule()
        elif c == ord('n'):
            self.random_rule()
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
            count = 0
            checkpoint = random.randint(rule_min, rule_max)
            self.pause = False
            while True:
                c = self.stdscr.getch()
                if count > checkpoint:
                    checkpoint = random.randint(rule_min, rule_max)
                    count = 0
                    c = ord('n')
                self.act(c)
                time.sleep(self.wait_time)
                count += 1
            time.sleep(1)
        finally:
            self.stop()

if __name__ == "__main__":
    print sys.argv
    ca = ca_app(sys.argv[1])
