import json
import os
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QDialog, QMessageBox,
	QLabel, QTextEdit, QDateEdit
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

		self.dateEdit = QDateEdit()
		self.dateEdit.setCalendarPopup(True)
		self.dateEdit.setDate(QDate.currentDate())
		self.headLayout.addWidget(QLabel("Due Date:"))
		self.headLayout.addWidget(self.dateEdit)

		self.layout.addLayout(self.headLayout)
		self.layout.addStretch()

		self.textInput = QTextEdit()
		self.layout.addWidget(self.textInput, stretch=1)

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
		details = self.textInput.toPlainText()
		dueDate = self.dateEdit.date().toString("yyyy-MM-dd")
		if not heading.strip():
			QMessageBox.warning(self, "Warning", "Heading cannot be empty!")
			return
		self.saved = True
		self.taskData = (heading, details, dueDate)
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
	def __init__(self, index, task, main_window):
		super().__init__()

		self.setWindowTitle(f"Task Details {task['heading'][:12]}{'...' if len(task['heading']) > 12 else ''}")
		self.resize(400, 300)

		self.index = index
		self.task = task
		self.main_window = main_window

		layout = QVBoxLayout()

		# Heading Display
		headLayout = QHBoxLayout()
		headLayout.addWidget(QLabel("Heading:").setStyleSheet("font-weight: bold"))
		headLayout.addWidget(QLabel(f"{task['heading']}"))
		self.dateEdit = QLabel(f"Due Date: {task.get('dueDate', 'not-set')}")
		headLayout.addWidget(self.dateEdit)
		layout.addLayout(headLayout)

		layout.addStretch()

		# Task Details
		self.detailsText = QTextEdit()
		self.detailsText.setPlainText(task["details"])
		self.detailsText.setReadOnly(True)
		layout.addWidget(self.detailsText, stretch=1)

		# buttons: edit delete back
		buttonLayout = QHBoxLayout()
		self.editbutton = QPushButton("Edit")
		self.deletebutton = QPushButton("Delete")
		self.backbutton = QPushButton("Back")

		buttonLayout.addWidget(self.editbutton)
		buttonLayout.addWidget(self.deletebutton)
		buttonLayout.addWidget(self.backbutton)

		layout.addLayout(buttonLayout)
		self.setLayout(layout)

		# connections
		self.editbutton.clicked.connect(self.editTask)
		self.deletebutton.clicked.connect(self.deleteTask)
		self.backbutton.clicked.connect(self.close)

	def deleteTask(self):
		confirm = QMessageBox.question(
			self, "Delete Task?", "Are you sure you want to delete this task?",
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		if confirm == QMessageBox.StandardButton.Yes:
			del self.main_window.tasks[self.index]
			self.main_window.taskList.takeItem(self.index)
			self.main_window.saveTasks()
			self.close()

	def editTask(self):
		# open Note with existing data
		editDialog = Note(self)
		editDialog.heading.setText(self.task['heading'])
		editDialog.textInput.setText(self.task['details'])

		if editDialog.exec():
			if editDialog.saved:
				heading, details, dueDate = editDialog.taskData
				# update task
				self.task['heading'] = heading
				self.task['details'] = details
				self.task['dueDate'] = dueDate
				self.main_window.tasks[self.index] = self.task
				self.main_window.taskList.item(self.index).setText(heading)
				self.main_window.saveTasks()
				# update this window
				self.detailsText.setPlainText(details)
				self.dateEdit.setText(dueDate)
				self.setWindowTitle(f"Task Details {self.task['heading'][:12]}{'...' if len(self.task['heading']) > 12 else ''}")


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

		self.searchBox = QLineEdit()
		self.searchBox.setPlaceholderText("Search Tasks...")
		self.searchBox.textChanged.connect(self.filterTasks)
		self.layout.insertWidget(1, self.searchBox)

		self.layout.addWidget(self.taskList)

		self.setLayout(self.layout)

		self.newTaskButton.clicked.connect(self.openNote)
		self.exitButton.clicked.connect(self.confirmExit)
		self.taskList.itemClicked.connect(self.viewTaskDetails)

		# --Important--
		# Keep references to opened windows to prevent them from being garbage collected
		# Adding a list to store open TaskView instances:
		self.openViews = []

	def filterTasks(self, text):
		self.taskList.clear()
		for task in self.tasks:
			heading = task["heading"]
			if text.lower() in heading.lower():
				itemText = heading
				self.taskList.addItem(itemText)

	def openNote(self):
		note = Note(self)
		if note.exec():
			# if user clicked save
			if note.saved:
				heading, details, dueDate = note.taskData
				self.tasks.append({"heading":heading, "details":details, "dueDate":dueDate, "Completed":False})
				self.taskList.addItem(heading)
				self.saveTasks()
				print(f"saved task:: {heading} - {details}...")

	def viewTaskDetails(self, item):
		index = self.taskList.row(item)
		task = self.tasks[index]
		view = TaskView(index, task, self)
		# view.exec()	# this line freezes the main thread untill window is closed
		view.show() 	# lets the user interact with multiple windows at the same time.
		self.openViews.append(view)

	def confirmExit(self):
		reply = QMessageBox.question(
			self, "Exit?", "Are you Sure?\nUnsaved changes will be Lost",
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		if reply == QMessageBox.StandardButton.Yes:
			# Option 1 — clean quit ===>>QApplication.quit()
			# Option 2 — let close event propagate
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

