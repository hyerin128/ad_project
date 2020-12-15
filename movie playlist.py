from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout

from keypad import genre

import time
from selenium import webdriver

import requests
from bs4 import BeautifulSoup

raw = requests.get("https://movie.naver.com/movie/running/current.nhn", headers={"User-Agent": "Mozilla/5.0"})

html = BeautifulSoup(raw.text, 'html.parser')
movies = html.select("dl.lst_dsc")


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

        genreLayout = QGridLayout()

        buttonGroups = {
            'genre': {'buttons': genre, 'layout': genreLayout, 'columns': 4},
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

        mainLayout.addLayout(genreLayout, 0, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle('my own playlist !')


    def buttonClicked(self):

        button = self.sender()
        key = button.text()

        for m in movies:

            title = m.select_one("dt.tit a").text
            genre = m.select_one("dl.lst_dsc dl.info_txt1 dd:nth-of-type(1) span.link_txt")

            if key not in genre.text:
                continue

            driver = webdriver.Chrome('chromedriver')
            driver.get("https://www.youtube.com/results?search_query=" + title + ' 예고편')
            time.sleep(1)

            continue_link = driver.find_element_by_partial_link_text(title)
            continue_link.click()

            break

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())