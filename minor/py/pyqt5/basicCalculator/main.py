import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from calc import Ui_MainWindow  # make sure the filename matches

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind_events()
        self.expression = ""

    def bind_events(self):
        # Connect all buttons to a single handler
        buttons = [
            self.ui.pushButton,    # 7
            self.ui.pushButton_2,  # 8
            self.ui.pushButton_3,  # 9
            self.ui.pushButton_9,  # 4
            self.ui.pushButton_10, # 5
            self.ui.pushButton_11, # 6
            self.ui.pushButton_13, # 1
            self.ui.pushButton_14, # 2
            self.ui.pushButton_15, # 3
            self.ui.pushButton_18, # 0

            self.ui.pushButton_4,  # /
            self.ui.pushButton_12, # *
            self.ui.pushButton_16, # -
            self.ui.pushButton_20, # +
        ]

        for button in buttons:
            button.clicked.connect(lambda _, b=button: self.button_pressed(b.text()))

        self.ui.pushButton_17.clicked.connect(self.clear)
        self.ui.pushButton_19.clicked.connect(self.evaluate)

    def button_pressed(self, text):
        self.expression += text
        self.ui.textfield.setText(self.expression)

    def clear(self):
        self.expression = ""
        self.ui.textfield.setText("")

    def evaluate(self):
        try:
            result = str(eval(self.expression))
            self.ui.textfield.setText(result)
            self.expression = result
        except Exception:
            self.ui.textfield.setText("Error")
            self.expression = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CalculatorApp()
    win.show()
    sys.exit(app.exec_())

