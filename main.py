# Máquina de turing para trabalho de 6 fase de Ciência da Computação
# Autor: Gustavo Niehues

import instrucoes
import sys
import turingmachine

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
	QTableWidget, QTableWidgetItem

qt_app = QApplication(sys.argv)


class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Turing Machine')
		self.setMinimumHeight(600)
		self.maquina_passoapasso = Executar()
		self.maquina = turingmachine.TuringMachine
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

		self.caixa_interface = QVBoxLayout()
		self.caixa_interface.addLayout(caixa_configuracoes)
		self.tabela()
		botao_passoapasso = QPushButton('Execução passo a passo')
		botao_passoapasso.clicked.connect(self.exec_passoapasso)
		botao_direto = QPushButton('Execução direta')
		botao_direto.clicked.connect(self.exec_direto)
		caixa_execucao = QHBoxLayout()
		caixa_execucao.addWidget(botao_direto)
		caixa_execucao.addWidget(botao_passoapasso)
		self.caixa_interface.addLayout(caixa_execucao)
		self.texto_resultado = QLabel('')
		self.texto_resultado.setStyleSheet('font: 14pt')
		self.caixa_interface.addWidget(self.texto_resultado)
		self.gerar_instrucao()
		self.caixa_observacoes = QVBoxLayout()
		self.setLayout(self.caixa_interface)

	def tabela(self):
		# TODO: botoes de adicionar ou excluir linhas
		self.tabela = QTableWidget()
		botao_adicionarlinha = QPushButton('Adicionar Linha')
		botao_excluirlinha = QPushButton('Excluir Linha')
		caixa_botoestabela = QHBoxLayout()
		caixa_botoestabela.addWidget(botao_adicionarlinha)
		caixa_botoestabela.addWidget(botao_excluirlinha)
		self.caixa_interface.addLayout(caixa_botoestabela)
		self.caixa_interface.addWidget(self.tabela)
		self.tabela.setColumnCount(5)
		self.tabela.setRowCount(6)
		self.tabela.verticalHeader().hide()
		self.tabela.horizontalHeader().hide()
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

	def recolher_dados(self):
		instrucoes = {}
		colunas = 5
		linhas = self.tabela.rowCount()
		for linha in range(1, linhas):
			chave = ()
			lista_chave = []
			instrucao = []
			for coluna in range(colunas):
				if coluna < 2:
					lista_chave.append((self.tabela.item(linha, coluna)).text())
				else:
					instrucao.append((self.tabela.item(linha, coluna)).text())
			chave = tuple(lista_chave)
			instrucoes[chave] = instrucao
		fita = self.entrada_fita.text()
		return fita, instrucoes

	def exec_direto(self):
		fita, instrucoes = self.recolher_dados()
		if fita is not '':
			self.texto_resultado.setText('Resultado: {0}'.format(self.maquina.start(fita, instrucoes)))
		else:
			self.texto_resultado.setText('Entrada de fita vazia')

	def exec_passoapasso(self):
		fita, instrucoes = self.recolher_dados()
		self.maquina_passoapasso.run(fita, instrucoes)

	def gerar_instrucao(self):
		lista_instrucoes = instrucoes.multiplicacao
		self.tabela.setRowCount(len(lista_instrucoes) + 1)
		self.tabela.clear()
		cont = 1
		self.tabela.setItem(0, 0, QTableWidgetItem('Instrução'))
		self.tabela.setItem(0, 1, QTableWidgetItem('Leitura'))
		self.tabela.setItem(0, 2, QTableWidgetItem('Próximo passo'))
		self.tabela.setItem(0, 3, QTableWidgetItem('Substituir'))
		self.tabela.setItem(0, 4, QTableWidgetItem('Direçao (E ou D)'))
		for instrucao in lista_instrucoes:
			chave = lista_instrucoes[instrucao]
			self.tabela.setItem(cont, 0, QTableWidgetItem(instrucao[0]))
			self.tabela.setItem(cont, 1, QTableWidgetItem(instrucao[1]))
			self.tabela.setItem(cont, 2, QTableWidgetItem(chave[0]))
			self.tabela.setItem(cont, 3, QTableWidgetItem(chave[1]))
			self.tabela.setItem(cont, 4, QTableWidgetItem(chave[2]))
			cont = cont + 1

	def run(self):
		self.show()
		qt_app.exec_()


class Executar(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Executar')
		self.setMinimumWidth(600)
		self.fita = None
		self.instrucoes = None
		self.maquina = turingmachine.TuringMachine()
		self.tabela_fita = QTableWidget(2, 100)
		self.tabela_fita.horizontalHeader().hide()
		self.tabela_fita.verticalHeader().hide()
		self.tabela_fita.setStyleSheet('font: 14pt')
		for i in range(self.tabela_fita.columnCount()):
			self.tabela_fita.setColumnWidth(i, 20)

		self.botao_proximopasso = QPushButton('Próximo passo')
		self.botao_proximopasso.clicked.connect(self.proximoPasso)
		self.botao_passoapasso_1s = QPushButton('Resumir processo (1s/passo)')

		self.caixa_execucao = QHBoxLayout()
		self.caixa_execucao.addWidget(self.botao_proximopasso)
		self.caixa_execucao.addWidget(self.botao_passoapasso_1s)
		layout = QVBoxLayout()
		layout.addWidget(self.tabela_fita)
		layout.addLayout(self.caixa_execucao)
		self.setLayout(layout)

	def proximoPasso(self):
		fita, posicao_cabeca, estado_atual = self.maquina.operacao()
		self.gerar_tabela()
		self.tabela_fita.setItem(1, posicao_cabeca, QTableWidgetItem(estado_atual))

	def gerar_tabela(self):
		self.tabela_fita.clearContents()
		self.tabela_fita.setColumnCount(len(self.fita))
		for i in range(len(self.fita)):
			self.tabela_fita.setItem((0, i, QTableWidgetItem(self.fita[i])))

	def run(self, fita, instrucoes):
		self.fita = list(fita)
		self.instrucoes = instrucoes
		self.gerar_tabela()
		self.instrucoes = instrucoes
		self.maquina.limparMaquina()
		self.maquina.entrada_info(self.fita, self.instrucoes)
		self.show()
		for i in range(len(fita)):
			self.tabela_fita.setItem(0, i, QTableWidgetItem(self.fita[i]))
		self.tabela_fita.setItem(1,0, QTableWidgetItem('q0'))


Window().run()
