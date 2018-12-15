#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QFile, QObject
from PySide2.QtGui import QColor
from pyswip import Prolog

class Form(QObject):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        # Open ui file.
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        # Load ui file into the current form
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # Connect events
        solveBtn = self.window.findChild(QPushButton, 'solveBtn')
        solveBtn.clicked.connect(self.ok_handler)

        resetBtn = self.window.findChild(QPushButton, 'resetBtn')
        resetBtn.clicked.connect(self.reset_handler)

        # Find board objects
        self.topLeft = self.window.findChild(QTableWidget, 'topLeft')
        self.topMiddle = self.window.findChild(QTableWidget, 'topMiddle')
        self.topRight = self.window.findChild(QTableWidget, 'topRight')
        self.middleLeft = self.window.findChild(QTableWidget, 'middleLeft')
        self.middleMiddle = self.window.findChild(QTableWidget, 'middleMiddle')
        self.middleRight = self.window.findChild(QTableWidget, 'middleRight')
        self.bottomLeft = self.window.findChild(QTableWidget, 'bottomLeft')
        self.bottomMiddle = self.window.findChild(QTableWidget, 'bottomMiddle')
        self.bottomRight = self.window.findChild(QTableWidget, 'bottomRight')

        # Start prolog engine
        self.prolog = Prolog()
        self.prolog.consult("solver.pl")

        self.window.show()

    def ok_handler(self):
        puzzle = [[self.get_value_at(x,y) for y in range(9)] for x in range(9)]
        solution = self.solve_puzzle(puzzle)
        if solution != False:
            for y in range(9):
                for x in range(9):
                    self.set_value_at(y, x, solution[y][x])
            self.window.update()
        else:
            print("You fucked up")

    def get_item_value(self, item):
        if(hasattr(item, 'text')):
            if item.text() != ' ' and item.text() != '':
                return int(item.text())
            else:
                return 0
        else:
            return 0

    def get_value_at(self, x, y):
        horizontal = int(y / 3)
        horizontalIndex = y % 3
        vertical = int(x / 3)
        verticalIndex = x % 3

        if vertical == 0:
            if horizontal == 0:
                return self.get_item_value(self.topLeft.item(verticalIndex, horizontalIndex))
            elif horizontal == 1:
                return self.get_item_value(self.topMiddle.item(verticalIndex, horizontalIndex))
            else:
                return self.get_item_value(self.topRight.item(verticalIndex, horizontalIndex))
        elif vertical == 1:
            if horizontal == 0:
                return self.get_item_value(self.middleLeft.item(verticalIndex, horizontalIndex))
            elif horizontal == 1:
                return self.get_item_value(self.middleMiddle.item(verticalIndex, horizontalIndex))
            else:
                return self.get_item_value(self.middleRight.item(verticalIndex, horizontalIndex))
        else:
            if horizontal == 0:
                return self.get_item_value(self.bottomLeft.item(verticalIndex, horizontalIndex))
            elif horizontal == 1:
                return self.get_item_value(self.bottomMiddle.item(verticalIndex, horizontalIndex))
            else:
                return self.get_item_value(self.bottomRight.item(verticalIndex, horizontalIndex))

    def set_item_value(self, item, value):
        if (hasattr(item, 'text')):
            if item.text() != ' ' and item.text() != '':
                item.setText(value)
            else:
                item.setText(value)
                item.setTextColor(QColor("green"))
        else:
            item = QTableWidgetItem(value)
            item.setTextColor(QColor("green"))

    def set_value_at(self, x, y, value):
        nvalue = str(value)
        newItem = QTableWidgetItem(nvalue)
        current_value = self.get_value_at(x, y)
        if current_value != 0:
            newItem.setTextColor(QColor("green"))

        horizontal = int(y / 3)
        horizontalIndex = y % 3
        vertical = int(x / 3)
        verticalIndex = x % 3

        if vertical == 0:
            if horizontal == 0:
                self.topLeft.setItem(verticalIndex, horizontalIndex, newItem)
            elif horizontal == 1:
                self.topMiddle.setItem(verticalIndex, horizontalIndex, newItem)
            else:
                self.topRight.setItem(verticalIndex, horizontalIndex, newItem)
        elif vertical == 1:
            if horizontal == 0:
                self.middleLeft.setItem(verticalIndex, horizontalIndex, newItem)
            elif horizontal == 1:
                self.middleMiddle.setItem(verticalIndex, horizontalIndex, newItem)
            else:
                self.middleRight.setItem(verticalIndex, horizontalIndex, newItem)
        else:
            if horizontal == 0:
                self.bottomLeft.setItem(verticalIndex, horizontalIndex, newItem)
            elif horizontal == 1:
                self.bottomMiddle.setItem(verticalIndex, horizontalIndex, newItem)
            else:
                self.bottomRight.setItem(verticalIndex, horizontalIndex, newItem)

    def reset_handler(self):
        self.topLeft.clearContents()
        self.topMiddle.clearContents()
        self.topRight.clearContents()
        self.middleLeft.clearContents()
        self.middleMiddle.clearContents()
        self.middleRight.clearContents()
        self.bottomLeft.clearContents()
        self.bottomMiddle.clearContents()
        self.bottomRight.clearContents()

    def solve_puzzle(self, puzzle):
        p = str(puzzle).replace("0", "_")
        result = list(self.prolog.query("L=%s,solve_sudoku(L)" % p, maxresult=1))
        if result:
            result = result[0]
            return result['L']
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('dialog.ui')
    sys.exit(app.exec_())
