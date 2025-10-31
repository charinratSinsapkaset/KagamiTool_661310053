try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os
import importlib
from . import mirToolUtil as util
importlib.reload(util)

ROOT_RESOURCE_DIR = r'C:/Users/Choyuusama/OneDrive/Documents/maya/2024/scripts/MirrorTool_02/resources'


class MirrorDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('KAGAMI_TOOL')
		self.resize(300, 300)

		# Style
		self.setStyleSheet('''
			background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
				stop:0 #D5DEEF, stop:1 #8AAEE0, stop:2 #8AAEE0);
		''')

		# Main layout
		self.mainLayout = QtWidgets.QVBoxLayout(self)
		self.mainLayout.setContentsMargins(10, 10, 10, 10)
		self.mainLayout.setSpacing(10)

		# Image
		self.imageLabel = QtWidgets.QLabel()
		image_path = os.path.join(ROOT_RESOURCE_DIR, "images", "001.png")
		if os.path.exists(image_path):
			pixmap = QtGui.QPixmap(image_path).scaled(
				128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			self.imageLabel.setPixmap(pixmap)
		else:
			self.imageLabel.setText("Image not found")
			self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.mainLayout.addWidget(self.imageLabel)


		# === X ===
		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.plusXButton = QtWidgets.QPushButton('X+')
		self.plusXButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #283861;
					color: white;
					border-radius: 5px;
					font-size: 16px;
					padding: 10px;
					font-family: default;
					font-weight: 10px;
				}
				QPushButton:hover {
					background-color: #8AAEE0;
				}
				QPushButton:pressed {
					background-color: navy;
				}
			'''
		)

		self.minusXButton = QtWidgets.QPushButton('X-')
		self.minusXButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #283861;
					color: white;
					border-radius: 5px;
					font-size: 16px;
					padding: 10px;
					font-family: default;
					font-weight: 10px;
				}
				QPushButton:hover {
					background-color: #8AAEE0;
				}
				QPushButton:pressed {
					background-color: navy;
				}
			'''
		)
		self.buttonLayout.addWidget(self.plusXButton)
		self.buttonLayout.addWidget(self.minusXButton)

		# === Y ===
		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.plusYButton = QtWidgets.QPushButton('Y+')
		self.plusYButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #283861;
					color: white;
					border-radius: 5px;
					font-size: 16px;
					padding: 10px;
					font-family: default;
					font-weight: 10px;
				}
				QPushButton:hover {
					background-color: #8AAEE0;
				}
				QPushButton:pressed {
					background-color: navy;
				}
			'''
		)

		self.minusYButton = QtWidgets.QPushButton('Y-')
		self.minusYButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #283861;
					color: white;
					border-radius: 5px;
					font-size: 16px;
					padding: 10px;
					font-family: default;
					font-weight: 10px;
				}
				QPushButton:hover {
					background-color: #8AAEE0;
				}
				QPushButton:pressed {
					background-color: navy;
				}
			'''
		)
		self.buttonLayout.addWidget(self.plusYButton)
		self.buttonLayout.addWidget(self.minusYButton)

		# === z ===
		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.plusZButton = QtWidgets.QPushButton('Z+')
		self.plusZButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #283861;
					color: white;
					border-radius: 5px;
					font-size: 16px;
					padding: 10px;
					font-family: default;
					font-weight: 10px;
				}
				QPushButton:hover {
					background-color: #8AAEE0;
				}
				QPushButton:pressed {
					background-color: navy;
				}
			'''
		)

		self.minusZButton = QtWidgets.QPushButton('Z-')
		self.minusZButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #283861;
					color: white;
					border-radius: 5px;
					font-size: 16px;
					padding: 10px;
					font-family: default;
					font-weight: 10px;
				}
				QPushButton:hover {
					background-color: #8AAEE0;
				}
				QPushButton:pressed {
					background-color: navy;
				}
			'''
		)
		self.buttonLayout.addWidget(self.plusZButton)
		self.buttonLayout.addWidget(self.minusZButton)

		self.mainLayout.addStretch()

		# Rotate input
		angleLayout = QtWidgets.QHBoxLayout()
		angleLabel = QtWidgets.QLabel("Rotate:")
		self.angleField = QtWidgets.QDoubleSpinBox()
		self.angleField.setDecimals(2)
		self.angleField.setRange(-9999, 9999)
		self.angleField.setValue(0.0)
		self.angleField.setMinimumWidth(150)
		angleLayout.addWidget(angleLabel)
		angleLayout.addWidget(self.angleField)
		self.mainLayout.addLayout(angleLayout)

		self.mainLayout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.HLine))

		# Clean button
		self.cleanButton = QtWidgets.QPushButton('Clean Mirror!')
		self.cleanButton.setStyleSheet('''
			QPushButton {
				background-color: #283861;
				color: white;
				font-weight: bold;
				padding: 6px;
				border-radius: 5px;
			}
			QPushButton:hover {
				background-color: #8AAEE0;
			}
		'''
		)
		self.mainLayout.addWidget(self.cleanButton)

		# debug: show MIR methods on instance (temporary)
		print("DEBUG MirrorDialog methods:", [n for n in dir(self) if n.startswith('MIR')])

		# Connections
		self.plusXButton.clicked.connect(self.MIRplusX)
		self.minusXButton.clicked.connect(self.MIRminusX)
		self.plusYButton.clicked.connect(self.MIRplusY)
		self.minusYButton.clicked.connect(self.MIRminusY)
		self.plusZButton.clicked.connect(self.MIRplusZ)
		self.minusZButton.clicked.connect(self.MIRminusZ)
		self.cleanButton.clicked.connect(self.onClean)

	# --- methods MUST be indented inside class ---
	def MIRplusX(self):
		util.mirrorMinusZ()

	def MIRminusX(self):
		util.mirrorPlusZ()

	def MIRplusY(self):
		util.mirrorMinusX()

	def MIRminusY(self):
		util.mirrorPlusX()

	def MIRplusZ(self):
		util.mirrorMinusY()

	def MIRminusZ(self):
		util.mirrorPlusY()




	def onClean(self):
		util.mirrorCleanAll()


def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = MirrorDialog(parent=ptr)
	ui.show()
