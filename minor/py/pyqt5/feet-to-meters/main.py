import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from converter_ui import Ui_MainWindow

class ConvertApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# when radio buttons toggeld
		self.feetToMeterRadio.toggled.connect(self.update_labels)
		self.meterToFeetRadio.toggled.connect(self.update_labels)

		# connect the button
		self.convertButton.clicked.connect(self.convert_units)

		# Quit
		## self.quitButton.clicked.connect(self.close)
		self.quitButton.clicked.connect(self.confirm_quit)

	def confirm_quit(self):
		reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
		if reply ==QMessageBox.Yes:
			self.close()

	def update_labels(self):
		if self.feetToMeterRadio.isChecked():
			self.label.setText("Feet")
			self.label_3.setText("Meters")
			self.convert_units()
		elif self.meterToFeetRadio.isChecked():
			self.label.setText("Meters")
			self.label_3.setText("Feet")
			self.convert_units()

	def convert_units(self):
		try:
			value = float(self.inputField.text())
			if self.feetToMeterRadio.isChecked():
				result = value * 0.3048
				self.resultLabel.setText(f"{result:.4f}")
			elif self.meterToFeetRadio.isChecked():
				result = value / 0.3048
				self.resultLabel.setText(f"{result:.4f}")
			else:
				self.resultLabel.setText("Select a conversion.")

		except ValueError:
			self.ui.label_result.setText("Invalid Input")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = ConvertApp()
	window.show()
	sys.exit(app.exec_())
