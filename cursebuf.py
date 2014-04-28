#!/usr/bin/env python

class cursebuf:
    def __init__(self, lines):
        self.lines = []
        print "len(lines): {0}".format(lines)
        for n in range(lines):
            self.lines.append("")

    def get_line(self, line):
        return self.lines[line]

    def add_line(self, line):
        self.lines.pop()
        self.lines.insert(0, line)

    def get_buf(self):
        return self.lines
