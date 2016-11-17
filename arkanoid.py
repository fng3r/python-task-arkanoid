import sys
import os.path
from PyQt5.QtWidgets import (QApplication,
                             QPushButton,
                             QLineEdit,
                             QVBoxLayout,
                             QStackedLayout,
                             QWidget,
                             QDesktopWidget)
from PyQt5.QtGui import QPainter, QImage, QBrush, QPalette, QFont, QColor
from PyQt5.QtCore import Qt, QRect, QTimer
from game import GameModel
from core import Size


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(self.screen.width(), self.screen.height() - 70)

        self.in_game = False
        self.is_game_finished = False
        self.left = False
        self.right = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.setWindowTitle('Arkanoid')

        self.main_menu = QWidget(self)
        self.game_widget = QWidget(self)

        palette = QPalette()
        palette.setBrush(self.backgroundRole(),
                         QBrush(QImage(os.path.join('images', 'space.png'))))
        self.setPalette(palette)

        self.game = GameModel(Size(self.width(), self.height()))

        self.painter = QPainter()

        self.stacked = QStackedLayout(self)
        self.stacked.addWidget(self.game_widget)
        self.set_main_menu_layout()
        self.stacked.setCurrentWidget(self.main_menu)

        self.show()

    def start(self):
        self.game = GameModel(Size(self.width(), self.height()))
        self.change_current_widget(self.game_widget)
        self.timer.start(5)

    def tick(self):
        turn_rate = 1 if self.right else -1 if self.left else 0
        self.game.tick(turn_rate)
        self.repaint()

    def change_current_widget(self, widget):
        self.in_game = widget == self.game_widget
        self.stacked.setCurrentWidget(widget)
        self.update()

    def set_main_menu_layout(self):
        vbox = QVBoxLayout(self.main_menu)

        self.add_button('Start', self.start, vbox)

        vbox.setAlignment(Qt.AlignCenter)
        self.stacked.addWidget(self.main_menu)

    def keyPressEvent(self, event):
        key = event.key()
        self.left = key == Qt.Key_Left
        self.right = key == Qt.Key_Right
        if key == Qt.Key_Escape:
            self.timer.stop()
            self.change_current_widget(self.main_menu)
        if key == Qt.Key_Space:
            self.game.release_ball()
        if key == Qt.Key_X:
            self.game.shooting()

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.left = False
        if key == Qt.Key_Right:
            self.right = False

    def paintEvent(self, event):
        if self.in_game:
            self.painter.begin(self)
            self.draw()
            self.painter.end()

    def draw(self):
        self.painter.setFont(QFont('Arial', 20))
        self.painter.setPen(QColor('yellow'))
        self.painter.drawText(0, 20, 'Scores: %s' % str(self.game.scores))

        game = self.game
        self.painter.drawLine(game.frame.left, game.deadly_height,
                              game.frame.right, game.deadly_height)
        if self.game.gameover:
            return

        life_img = QImage(os.path.join('images', 'lifebonus.png'))
        draw_x = self.width() - life_img.width()
        draw_y = 0
        for _ in range(self.game.lives):
            self.painter.drawImage(draw_x, draw_y, life_img)
            draw_x -= life_img.width()

        self.painter.setRenderHint(self.painter.Antialiasing)

        for entity in self.game.get_entities():
            self.painter.drawImage(QRect(*entity.location,
                                         entity.frame.width,
                                         entity.frame.height),
                                   QImage(entity.get_image()))

    @staticmethod
    def add_button(text, callback, layout, alignment=Qt.AlignCenter):
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button, alignment=alignment)
        return button

    @staticmethod
    def add_line_edit(text, layout, value='', validator=None,
                      alignment=Qt.AlignCenter):
        edit = QLineEdit(str(value))
        edit.setPlaceholderText(text)
        if validator:
            edit.setValidator(validator)
        layout.addWidget(edit, alignment=alignment)
        return edit


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WINDOW = Window()
    APP.exec_()
