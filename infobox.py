#!/usr/bin/env python

import curses
import time

class infobox:
    def __init__(self, width, height, x, y):
        self.infowin = curses.newwin(height, width, y, x)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def update(self, rule, speed):
        self.infowin.erase()
        self.infowin.border()
        self.infowin.addstr(1,1, self.get_rule(rule))
        self.infowin.addstr(2,1, self.get_speed(speed))
        self.infowin.refresh()

    def get_rule(self, rule):
        return "rule:                {0}".format(rule)

    def get_speed(self, speed):
        return "lines per second:    {0:.2f}".format(speed)


if __name__ == "__main__":
    win = curses.initscr()
    win.keypad(1)
    win.border()
    ib = infobox(10,100,1,1)
    win.refresh()
    time.sleep(1)
    curses.nocbreak(); win.keypad(0); curses.echo()
    curses.endwin()
