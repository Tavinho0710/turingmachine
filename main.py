import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
	QTableWidget, QTableWidgetItem

qt_app = QApplication(sys.argv)

class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Turing Machine')

		texto_insirafita = QLabel('Insira a fita aqui:', self)
		self.entrada_fita = QLineEdit(self)
		caixa_insirafita = QVBoxLayout()
		caixa_insirafita.addWidget(texto_insirafita)
		caixa_insirafita.addWidget(self.entrada_fita)

		texto_listasimbolos = QLabel('Insira aqui a lista de simbolos separados por vírgula:')
		self.entrada_simbolos = QLineEdit(self)
		caixa_listasimbolos = QHBoxLayout()
		caixa_listasimbolos.addWidget(texto_listasimbolos)
		caixa_listasimbolos.addWidget(self.entrada_simbolos)

		texto_passos = QLabel('Quantidade de passos:')
		self.entrada_passos = QLineEdit()
		caixa_passos = QHBoxLayout()
		caixa_passos.addWidget(texto_passos)
		caixa_passos.addWidget(self.entrada_passos)

		gerar_tabela = QPushButton('Gerar tabela de instruções')
		gerar_tabela.clicked.connect(self.gerar_tabela)

		caixa_definesimbolos = QVBoxLayout()
		caixa_definesimbolos.addLayout(caixa_listasimbolos)
		caixa_definesimbolos.addLayout(caixa_passos)
		caixa_definesimbolos.addWidget(gerar_tabela)
		caixa_configuracoes = QHBoxLayout()
		caixa_configuracoes.addLayout(caixa_insirafita)
		caixa_configuracoes.addLayout(caixa_definesimbolos)
		self.caixa_geral = QVBoxLayout()
		self.caixa_geral.addLayout(caixa_configuracoes)
		self.tabela()
		self.setLayout(self.caixa_geral)

	def tabela(self):
		self.tabela = QTableWidget()
		botao_adicionarlinha = QPushButton('Adicionar Linha')
		botao_excluirlinha = QPushButton('Excluir Linha')
		caixa_botoestabela = QHBoxLayout()
		caixa_botoestabela.addWidget(botao_adicionarlinha)
		caixa_botoestabela.addWidget(botao_excluirlinha)
		self.caixa_geral.addLayout(caixa_botoestabela)
		self.caixa_geral.addWidget(self.tabela)
		self.tabela.setColumnCount(3)
		self.tabela.setRowCount(3)
		self.setMinimumHeight(600)
		self.setLayout(self.caixa_geral)

	def gerar_tabela(self):
		lista_simbolos = self.entrada_simbolos.text().split(',')
		passos = int(self.entrada_passos.text())

		self.tabela.setColumnCount((len(lista_simbolos) + 2))
		self.tabela.setRowCount((passos * len(lista_simbolos)) + 1)
		for i in range(len(lista_simbolos)):
			self.tabela.setItem(0, i + 2, QTableWidgetItem('{}'.format(lista_simbolos[i])))
		cont = 1
		for i in range(passos):
			for j in range(len(lista_simbolos)):
				self.tabela.setItem((cont), 0, QTableWidgetItem(('q{}'.format(i))))
				self.tabela.setItem((cont), 1, QTableWidgetItem(('{}'.format(lista_simbolos[j]))))
				cont = cont + 1

	def processar(self):
		pass
	def run(self):
		self.show()
		qt_app.exec_()

Window().run()