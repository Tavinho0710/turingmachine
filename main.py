from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QVBoxLayout, QHBoxLayout
import sys


qt_app = QApplication(sys.argv)

class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Turing Machine')
		self.setMinimumHeight(200)
		self.setMinimumWidth(200)

		texto_1 = QLabel('Insira a fita aqui:',self)
		entrada_fita = QLineEdit(self)
		texto_2 = QLabel('Insira aqui a lista de simbolos separados por vírgula:')
		entrada_simbolos = QLineEdit(self)
		layout_1 = QHBoxLayout()
		layout_1.addWidget(texto_1)
		layout_1.addWidget(entrada_fita)
		layout_1.
		layout_2 = QHBoxLayout()
		layout_2.addWidget(texto_2)
		layout_2.addWidget(entrada_simbolos)
		layout = QVBoxLayout()
		layout.addLayout(layout_1)
		layout.addLayout(layout_2)
		self.setLayout(layout)

	def run(self):
		self.show()
		qt_app.exec_()

Window().run()