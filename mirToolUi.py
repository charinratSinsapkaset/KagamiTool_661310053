try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os
from . import mirToolUtil as mutil

ROOT_RESOURCE_DIR = 'C:/Users/Choyuusama/OneDrive/Documents/maya/2024/scripts/MirrorTool/resources'

class MirrorDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle('KagamiTool')
		self.setFixedSize(200, 260)
		self.setStyleSheet('background-color: #3c3c3c; color: white;')
		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f"{ROOT_RESOURCE_DIR}/images/001.")
		scaled_pixmap = self.imagePixmap.scaled(
			QtCore.QSize(128,128),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation
			)

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(6, 6, 6, 6)
		self.main_layout.setSpacing(4)

		# === X Axis ===
		self.x_layout = QtWidgets.QHBoxLayout()
		self.plusX_btn = self.makeIconButton('plusX.png', '+X')
		self.minusX_btn = self.makeIconButton('minusX.png', '-X')
		self.x_layout.addWidget(self.plusX_btn)
		self.x_layout.addWidget(self.minusX_btn)
		self.main_layout.addLayout(self.x_layout)

		# === Y Axis ===
		self.y_layout = QtWidgets.QHBoxLayout()
		self.plusY_btn = self.makeIconButton('plusY.png', '+Y')
		self.minusY_btn = self.makeIconButton('minusY.png', '-Y')
		self.y_layout.addWidget(self.plusY_btn)
		self.y_layout.addWidget(self.minusY_btn)
		self.main_layout.addLayout(self.y_layout)

		# === Z Axis ===
		self.z_layout = QtWidgets.QHBoxLayout()
		self.plusZ_btn = self.makeIconButton('plusZ.png', '+Z')
		self.minusZ_btn = self.makeIconButton('minusZ.png', '-Z')
		self.z_layout.addWidget(self.plusZ_btn)
		self.z_layout.addWidget(self.minusZ_btn)
		self.main_layout.addLayout(self.z_layout)

		# === Done Clean Button ===
		self.clean_btn = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(ICON_PATH, 'Clean.png')), 'CleanMirror!')
		self.clean_btn.setStyleSheet('''
			QPushButton {
				background-color: #777;
				color: white;
				font-weight: bold;
				padding: 6px;
				border-radius: 4px;
			}
			QPushButton:hover {
				background-color: #999;
			}
		''')
		self.main_layout.addWidget(self.clean_btn)

		# === Connect Buttons ===
		self.plusX_btn.clicked.connect(lambda: self.handleMirror('+X'))
		self.minusX_btn.clicked.connect(lambda: self.handleMirror('-X'))
		self.plusY_btn.clicked.connect(lambda: self.handleMirror('+Y'))
		self.minusY_btn.clicked.connect(lambda: self.handleMirror('-Y'))
		self.plusZ_btn.clicked.connect(lambda: self.handleMirror('+Z'))
		self.minusZ_btn.clicked.connect(lambda: self.handleMirror('-Z'))


	def makeIconButton(self, icon_name, tooltip):
		btn = QtWidgets.QPushButton()
		btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, icon_name)))
		btn.setIconSize(QtCore.QSize(64, 64))
		btn.setFixedSize(80, 50)
		btn.setToolTip(f"{tooltip}  (Click = Mirror, Shift = Rotate)")
		btn.setStyleSheet('background-color: #2c2c2c; border: none;')
		return btn

	def handleMirror(self, axis):
		modifiers = QtWidgets.QApplication.keyboardModifiers()
		angle = self.rotate_field.value()
		if modifiers == QtCore.Qt.ShiftModifier:
			# Shift-click = rotate
			mutil.rotate(axis[-1], angle, negative="-" in axis)
		else:
			# Click = mirror
			mutil.mirror(axis)


def run():
	global ui
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = MirrorDialog(parent=ptr)
	ui.show()
