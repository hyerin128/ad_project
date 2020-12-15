from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout

from keypad import feeling, weather, situation

import time
from selenium import webdriver


class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calculator(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        feelingLayout = QGridLayout()
        weatherLayout = QGridLayout()
        situationLayout = QGridLayout()

        buttonGroups = {
            'feeling': {'buttons': feeling, 'layout': feelingLayout, 'columns': 3},
            'weather': {'buttons': weather, 'layout': weatherLayout, 'columns': 2},
            'situation': {'buttons': situation, 'layout': situationLayout, 'columns': 3},
        }

        for label in buttonGroups.keys():
            r = 0; c = 0
            buttonPad = buttonGroups[label]
            for btnText in buttonPad['buttons']:
                button = Button(btnText, self.buttonClicked)
                buttonPad['layout'].addWidget(button, r, c)
                c += 1
                if c >= buttonPad['columns']:
                    c = 0; r += 1

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addLayout(feelingLayout, 0, 0)
        mainLayout.addLayout(weatherLayout, 1, 0)
        mainLayout.addLayout(situationLayout, 2, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle('my own playlist !')


    def buttonClicked(self):

        button = self.sender()
        key = button.text()

        driver = webdriver.Chrome('chromedriver')

        driver.get("https://www.youtube.com/results?search_query=" + key +' 플레이리스트')
        time.sleep(1)

        continue_link = driver.find_element_by_partial_link_text(key)
        continue_link.click()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

