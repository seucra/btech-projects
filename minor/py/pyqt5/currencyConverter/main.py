import sys
import requests
from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)

class currencyConverter(QWidget):
        def __init__(self):
                super().__init__()
                self.setWindowTitle("Curency Converter")
                self.setGeometry(300,300,300,200)

                self.ammountInput = QLineEdit()
                self.ammountInput.setPlaceholderText("Enter Ammount")

                self.fromCurrency = QComboBox()
                self.toCurrency = QComboBox()

                self.resultLabel = QLabel("Converted ammount")
                self.convertButton = QPushButton("Convert")
                self.convertButton.clicked.connect(self.convertCurrency)

                layout = QVBoxLayout()
                layout.addWidget(QLabel("Ammount"))
                layout.addWidget(self.ammountInput)

                currencyLayout = QHBoxLayout()
                currencyLayout.addWidget(self.fromCurrency)
                currencyLayout.addWidget(self.toCurrency)
                layout.addLayout(currencyLayout)

                layout.addWidget(self.convertButton)
                layout.addWidget(self.resultLabel)

                self.setLayout(layout)
                self.loadCurrencies()

        def loadCurrencies(self):
                try:
                        response = requests.get("https://api.exchangerate.host/symbols")
                        data = response.json()
                        symbols = data["sysbols"]

                        currencyList = sorted(symbols.keys())

                        self.fromCurrency.setCurrentText("USD")
                        self.toCurrency.setCurrentText("INR")
                except Exception as e:
                        QMessageBox.critical(self, "Error", f":Failed to load currencies:\n{e}")

        def convertCurrency(self):
                try:
                        ammount = float(self.ammountInput.text())
                        fromC = self.fromCurrency.currentText()
                        toC = self.toCurrency.currentText()

                        url = f"https://api.exchangerate.host/convert?from={fromC}&to={toC}&amount={amount}"
                        response = request.get(url)
                        data = response.json()

                        if data.get("result") is not None:
                                result = round (data["result"], 2)
                                self.resultLabel.setText(f"{ammount} {fromC} = {result} {toC}")
                        else:
                                self.resultLabel.setText("Conversation Failed")
                except ValueError:
                        QMessageBox.warning(self, "Input Error", "please enter a valid number.")
                except Exception as e:
                        QMessageBox.critical(self, "Error", f":Conversation Failed:\n{e}")


if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = currencyConverter()
        window.show()
        sys.exit(app.exec_())
