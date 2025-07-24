import json
import os
from PyQt5.QtWidgets import (
QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QDialog, QMessageBox, QLabel, QTextEdit
)

TASKFILE = "tasks.json"

class Note(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("New Task")
		self.resize(400, 300)
		self.layout = QVBoxLayout()

		self.headLayout = QHBoxLayout()
		self.heading_label = QLabel("Heading:")
		self.headLayout.addWidget(self.heading_label)
		self.heading = QLineEdit()
		self.headLayout.addWidget(self.heading)
		self.layout.addLayout(self.headLayout)

		self.layout.addStretch()

		self.text_input = QTextEdit()
		self.layout.addWidget(self.text_input, stretch=1)

		self.buttonLayout = QHBoxLayout()
		self.saveButton = QPushButton("Save")
		self.discardButton = QPushButton("Discard")

		self.buttonLayout.addWidget(self.saveButton)
		self.buttonLayout.addWidget(self.discardButton)

		self.layout.addLayout(self.buttonLayout)

		self.setLayout(self.layout)

		self.saved = False

		# connect
		self.saveButton.clicked.connect(self.saveTask)
		self.discardButton.clicked.connect(self.discardTask)

	def saveTask(self):
		heading = self.heading.text()
		details = self.text_input.toPlainText()
		if not heading.strip():
			QMessageBox.warning(self, "Warning", "Heading cannot be empty!")
			return
		self.saved = True
		self.taskdata = (heading, details)
		self.accept()	# close dialog with accept

	def discardTask(self):
		reply = QMessageBox.question(
			self, "Exit?", "Are you Sure?\nUnsaved changes will be Lost",
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		if reply == QMessageBox.StandardButton.Yes:
			self.saved = False
			self.reject()	# close dialog with reject

class TaskView(QDialog):
	def __init__(self, heading, details):
		super().__init__()

		a = "..." if len(heading) > 10 else ""
		self.setWindowTitle(f"Task Details -{heading[:10]}{a}-")
		self.resize(400, 300)
		layout = QVBoxLayout()

		headLayout = QHBoxLayout()
		headLayout.addWidget(QLabel("Heading:"))
		headLayout.addWidget(QLabel(f" {heading}"))
		layout.addLayout(headLayout)

		layout.addStretch()

		details_text = QTextEdit()
		details_text.setPlainText(details)
		details_text.setReadOnly(True)

		layout.addWidget(details_text, stretch=1)

		buttonLayout = QHBoxLayout()
		backbutton = QPushButton("Back")
		layout.addWidget(backbutton)

		self.setLayout(layout)

		backbutton.clicked.connect(self.close)

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("To Do List --Main Window--")
		self.resize(800, 600)

		self.tasks = []
		self.taskList = QListWidget()
		self.loadTasks()

		self.layout = QVBoxLayout()

		self.buttons = QHBoxLayout()
		self.newTaskButton = QPushButton("New Task")
		self.exitButton = QPushButton("Exit")

		self.buttons.addWidget(self.newTaskButton)
		self.buttons.addWidget(self.exitButton)
		self.layout.addLayout(self.buttons)

		self.layout.addWidget(self.taskList)

		self.setLayout(self.layout)

		self.newTaskButton.clicked.connect(self.openNote)
		self.exitButton.clicked.connect(self.confirmExit)
		self.taskList.itemClicked.connect(self.viewTaskDetails)

		# --Important--
		# Keep references to opened windows to prevent them from being garbage collected
		# Adding a list to store open TaskView instances:
		self.openViews = []

	def openNote(self):
		note = Note(self)
		if note.exec():
			# if user clicked save
			if note.saved:
				heading, details = note.taskdata
				self.tasks.append({"heading":heading, "details":details})
				self.taskList.addItem(heading)
				self.saveTasks()
				print(f"saved task:: {heading} - {details}...")

	def viewTaskDetails(self, item):
		index = self.taskList.row(item)
		task = self.tasks[index]
		heading, details = task["heading"], task["details"]
		view = TaskView(heading,details)
		# view.exec()	# this line freezes the main thread untill window is closed
		view.show() 	# lets the user interact with multiple windows at the same time.
		self.openViews.append(view)

	def confirmExit(self):
		reply = QMessageBox.question(
			self, "Exit?", "Are you Sure?\nUnsaved changes will be Lost",
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		if reply == QMessageBox.StandardButton.Yes:
			self.close()

	def saveTasks(self):
		try:
			with open(TASKFILE, "w") as f:
				json.dump(self.tasks, f, indent=4)
		except Exception as e:
			QMessageBox.warning(self, "Error", f"Could not save tasks:\n\t{e}")

	def loadTasks(self):
		if os.path.exists(TASKFILE):
			try:
				with open(TASKFILE, "r") as f:
					self.tasks = json.load(f)
					for task in self.tasks:
						self.taskList.addItem(task["heading"])
			except Exception as e:
				QMessageBox.warning(self, "Error", f"Could not load tasks:\n\t{e}")

if __name__ == "__main__":
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()

