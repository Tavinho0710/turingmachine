import sys

from PyQt5.QtWidgets import QWidget, QApplication

import instrucoes


class Window(QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setWindowTitle('Turing Machine')

	def iniciar(self):
		fita = self.fita.get()
		resultado = self.maquina.start(fita, instrucoes.multiplicacao)


root = QApplication(sys.argv)
app = Window()
app.show()
sys.exit(root.exec_())
