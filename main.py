import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
	QTableWidget, QTableWidgetItem

qt_app = QApplication(sys.argv)


class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Turing Machine')
		self.e = Executar()
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
		botao_passoapasso = QPushButton('Execução passo a passo')
		botao_passoapasso.clicked.connect(self.processar)
		botao_direto = QPushButton('Execução contínua')
		caixa_execucao = QHBoxLayout()
		caixa_execucao.addWidget(botao_passoapasso)
		caixa_execucao.addWidget(botao_direto)
		self.caixa_geral.addLayout(caixa_execucao)
		self.setMinimumHeight(600)
		self.setLayout(self.caixa_geral)

	def tabela(self):
		# TODO: botoes de adicionar ou excluir linhas
		self.tabela = QTableWidget()
		botao_adicionarlinha = QPushButton('Adicionar Linha')
		botao_excluirlinha = QPushButton('Excluir Linha')
		caixa_botoestabela = QHBoxLayout()
		caixa_botoestabela.addWidget(botao_adicionarlinha)
		caixa_botoestabela.addWidget(botao_excluirlinha)
		self.caixa_geral.addLayout(caixa_botoestabela)
		self.caixa_geral.addWidget(self.tabela)
		self.tabela.setColumnCount(5)
		self.tabela.setRowCount(6)
		self.tabela.setItem(0, 0, QTableWidgetItem('Instrução'))
		self.tabela.setItem(0, 1, QTableWidgetItem('Leitura'))
		self.tabela.setItem(0, 2, QTableWidgetItem('Próximo passo'))
		self.tabela.setItem(0, 3, QTableWidgetItem('Substituir'))
		self.tabela.setItem(0, 4, QTableWidgetItem('Direçao (E ou D)'))
		self.tabela.setItem(1, 0, QTableWidgetItem('q0'))
		self.tabela.setItem(1, 1, QTableWidgetItem('>'))

	def gerar_tabela(self):
		lista_simbolos = self.entrada_simbolos.text().split(',')
		passos = int(self.entrada_passos.text())
		self.tabela.setRowCount((passos * len(lista_simbolos)) + 1)
		cont = 1
		for i in range(passos):
			for j in range(len(lista_simbolos)):
				self.tabela.setItem((cont), 0, QTableWidgetItem(('q{}'.format(i))))
				self.tabela.setItem((cont), 1, QTableWidgetItem(('{}'.format(lista_simbolos[j]))))
				cont = cont + 1

	def processar(self):
		instrucoes = {}
		colunas = self.tabela.columnCount()
		linhas = self.tabela.rowCount()
		for linha in range(1,linhas):
			chave = ()
			lista_chave = []
			instrucao = []
			for coluna in range(colunas):
				if coluna < 2:
					lista_chave.append((self.tabela.item(linha, coluna)).text())
				else:
					instrucao.append((self.tabela.item(linha, coluna)).text())
			chave = tuple(lista_chave)
			print(chave)
			instrucoes[chave] = instrucao
		print(instrucoes)
		self.e.show()

	def run(self):
		self.show()
		qt_app.exec_()


class Executar(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Executar')
		self.fita = QTableWidget(2,100)
		layout = QVBoxLayout()
		layout.addWidget(self.fita)
		self.setLayout(layout)


Window().run()
