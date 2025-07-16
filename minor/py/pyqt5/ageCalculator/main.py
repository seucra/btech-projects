import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QDate
from datetime import date
from calculateAge import Ui_MainWindow

class AgeApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.dateL.setMinimumDate(QDate(1900,1,1))
		self.dateL.setMaximumDate(QDate.currentDate())
		self.dateL.setDate(QDate(1900,1,1))

		self.dateL.setDisplayFormat("dd/MM/yyyy")

		# Connect button actions
		self.calcAge.clicked.connect(self.calculate_age)
		self.quitB.clicked.connect(self.quit)

	def quit(self):
		reply = QMessageBox.question(self, "Quit", "Are you sure you want to Quit?", QMessageBox.Yes | QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.close()

	def calculate_age(self):
		dob_qdate = self.dateL.date()
		dob = date(dob_qdate.year(), dob_qdate.month(), dob_qdate.day())

		today = date.today()

		# Calculate full years, months, days
		years = today.year - dob.year
		months = today.month - dob.month
		days = today.day - dob.day

		if days < 0:
			months -= 1
			prev_month = today.month -1 if today.month > 1 else 12
			prev_year = today.year if today.month > 1 else today.year -1
			days += (date(prev_year, prev_month %12 +1, 1) - date(prev_year, prev_month, 1)).days

		if months < 0:
			years -= 1
			months += 12


		self.outputL.setText(f"You are {years} years, {months} months, and {days} days old.")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = AgeApp()
	window.show()
	sys.exit(app.exec_())
