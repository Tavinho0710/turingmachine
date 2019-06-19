# Máquina de turing para trabalho de 6 fase de Ciência da Computação
# Autor: Gustavo Niehues e Welliton Serafim

import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
	QTableWidget, QTableWidgetItem

import instrucoes
import turingmachine

qt_app = QApplication(sys.argv)


class Window(QWidget):
	def __init__(self):

		QWidget.__init__(self)
		self.setWindowTitle('Turing Machine')
		self.setMinimumHeight(600)
		self.maquina_passoapasso = Executar()
		self.maquina = turingmachine.TuringMachine()
		texto_insirafita = QLabel('Insira a fita aqui:', self)
		self.entrada_fita = QLineEdit(self)
		caixa_insirafita = QVBoxLayout()
		caixa_insirafita.addWidget(texto_insirafita)
		caixa_insirafita.addWidget(self.entrada_fita)
		texto_insiraprimeirainstrucao = QLabel('Insira a primeira instrução:')
		self.entrada_primeirainstrucao = QLineEdit(self)
		self.entrada_primeirainstrucao.setText('q0')
		caixa_primeirainstrucao = QVBoxLayout()
		caixa_primeirainstrucao.addWidget(texto_insiraprimeirainstrucao)
		caixa_primeirainstrucao.addWidget(self.entrada_primeirainstrucao)
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

		caixa_entradas = QVBoxLayout()
		caixa_entradas.addLayout(caixa_insirafita)
		caixa_entradas.addLayout(caixa_primeirainstrucao)
		caixa_configuracoes = QHBoxLayout()
		caixa_configuracoes.addLayout(caixa_entradas)
		caixa_configuracoes.addLayout(caixa_definesimbolos)

		self.caixa_interface = QVBoxLayout()
		self.caixa_interface.addLayout(caixa_configuracoes)

		self.tabela()

		botao_passoapasso = QPushButton('Execução passo a passo')
		botao_direto = QPushButton('Execução direta')
		botao_passoapasso.clicked.connect(self.exec_passoapasso)
		botao_direto.clicked.connect(self.exec_direto)

		caixa_execucao = QHBoxLayout()
		caixa_execucao.addWidget(botao_direto)
		caixa_execucao.addWidget(botao_passoapasso)
		self.caixa_interface.addLayout(caixa_execucao)
		self.texto_resultado = QLabel('')
		self.texto_resultado.setStyleSheet('font: 14pt')

		observacao1 = QLabel('Instruções de uso:')
		observacao1.setWordWrap(True)
		observacao2 = QLabel('1) Para o funcionamento da máquina, cada linha de instrução utilizada deve ser '
		                     'totalmente preenchida.')
		observacao2.setWordWrap(True)
		observacao5 = QLabel('2) Toda linha com células não preenchidas será descartada, sem necessidade de remoção'
		                     ' manual')
		observacao5.setWordWrap(True)
		observacao3 = QLabel('3) Para casos de uso de espaços em instruções, clique no campo e dê um espaço,'
		                     ' não deixe em branco.')
		observacao3.setWordWrap(True)
		observacao4 = QLabel('4) Para a máquina detectar estado de parada, deve-se colocar \'END\' no campo de próximo '
		                     'passo da instrução final.')
		observacao4.setWordWrap(True)

		texto_geracao = QLabel('Instruções gravadas:')
		botao_soma = QPushButton('Adição')
		botao_soma.clicked.connect(lambda: self.gerar_instrucao(instrucoes.soma))
		botao_subtracao = QPushButton('Subtração')
		botao_subtracao.clicked.connect(lambda: self.gerar_instrucao(instrucoes.subtracao))
		botao_multiplicacao = QPushButton('Multiplicação')
		botao_multiplicacao.clicked.connect(lambda: self.gerar_instrucao(instrucoes.multiplicacao))
		botao_divisao = QPushButton('Divisão')
		botao_divisao.clicked.connect(lambda: self.gerar_instrucao(instrucoes.divisao))

		caixa_instrucoes = QVBoxLayout()
		caixa_instrucoes.addWidget(texto_geracao)
		caixa_instrucoes.addWidget(botao_soma)
		caixa_instrucoes.addWidget(botao_subtracao)
		caixa_instrucoes.addWidget(botao_multiplicacao)
		caixa_instrucoes.addWidget(botao_divisao)

		caixa_barralateral = QVBoxLayout()
		caixa_barralateral.addWidget(observacao1)
		caixa_barralateral.addWidget(observacao2)
		caixa_barralateral.addWidget(observacao5)
		caixa_barralateral.addWidget(observacao3)
		caixa_barralateral.addWidget(observacao4)
		caixa_barralateral.addLayout(caixa_instrucoes)

		caixa_geral = QHBoxLayout()
		caixa_geral.addLayout(self.caixa_interface, 3)
		caixa_geral.addLayout(caixa_barralateral)

		caixa_resultado = QVBoxLayout()
		caixa_resultado.addLayout(caixa_geral)
		caixa_resultado.addWidget(self.texto_resultado)
		self.setLayout(caixa_resultado)

	def tabela(self):
		self.tabela = QTableWidget()
		self.tabela.setHorizontalHeaderItem(0, QTableWidgetItem('Instrução'))
		botao_adicionarlinha = QPushButton('Adicionar Linha')
		botao_adicionarlinha.clicked.connect(self.adiciona_linha)
		botao_excluirlinha = QPushButton('Excluir Linha Selecionada')
		botao_excluirlinha.clicked.connect(self.excluir_linha)
		caixa_botoestabela = QHBoxLayout()
		caixa_botoestabela.addWidget(botao_adicionarlinha)
		caixa_botoestabela.addWidget(botao_excluirlinha)
		self.caixa_interface.addLayout(caixa_botoestabela)
		self.caixa_interface.addWidget(self.tabela)
		self.tabela.setColumnCount(5)
		self.tabela.setRowCount(6)
		hl = ['Instrução', 'Leitura', 'Próximo Passo', 'Substituir', 'Direção (E ou D)']
		self.tabela.setHorizontalHeaderLabels(hl)
		self.tabela.verticalHeader().hide()

	def excluir_linha(self):
		if self.tabela.currentRow():
			self.tabela.removeRow(self.tabela.currentRow())
		else:
			self.tabela.removeRow(self.tabela.rowCount() - 1)

	def adiciona_linha(self):
		if self.tabela.currentRow():
			self.tabela.insertRow(self.tabela.currentRow() + 1)
		else:
			self.tabela.insertRow(self.tabela.rowCount())

	def gerar_tabela(self):
		self.texto_resultado.clear()
		self.tabela.clearContents()
		try:
			if self.entrada_simbolos.text() and self.entrada_passos.text():
				lista_simbolos = self.entrada_simbolos.text().split(',')
				try:
					passos = int(self.entrada_passos.text())
				except:
					raise Exception('Valor para quantidade de passos deve ser inteiro')
				self.tabela.setRowCount((passos * len(lista_simbolos)))
				cont = 0
				for i in range(passos):
					for j in range(len(lista_simbolos)):
						self.tabela.setItem(cont, 0, QTableWidgetItem(('q{}'.format(i))))
						self.tabela.setItem(cont, 1, QTableWidgetItem(('{}'.format(lista_simbolos[j]))))
						cont = cont + 1
			else:
				raise Exception('Um ou mais campos não estão preenchidos para a geração da tabela')
		except Exception as e:
			self.texto_resultado.setText('Erro: {}'.format(e))

	def recolher_dados(self):
		instrucoes = {}
		colunas = 5
		linhas = self.tabela.rowCount()
		for linha in range(0, linhas):
			lista_chave = []
			instrucao = []
			valido = True
			for coluna in range(colunas):
				if self.tabela.item(linha, coluna) and self.tabela.item(linha, coluna).text():
					if coluna < 2:
						lista_chave.append((self.tabela.item(linha, coluna)).text())
					else:
						instrucao.append((self.tabela.item(linha, coluna)).text())
				else:
					valido = False
					continue
			chave = tuple(lista_chave)
			if valido:
				instrucoes[chave] = instrucao
		fita = self.entrada_fita.text()
		instrucao_inicial = self.entrada_primeirainstrucao.text()
		return fita, instrucoes, instrucao_inicial

	def exec_direto(self):
		self.texto_resultado.clear()
		fita, instrucoes, instrucao_inicial = self.recolher_dados()
		try:
			if not fita:
				raise Exception('Fita não detectada')
			self.maquina.entrada_info(list(fita), instrucoes, instrucao_inicial)
			self.texto_resultado.setText('Resultado: {0}'.format(self.maquina.start()))
		except Exception as e:
			self.texto_resultado.setText('Erro: {}'.format(e))

	def exec_passoapasso(self):
		fita, instrucoes, instrucao_inicial = self.recolher_dados()
		try:
			self.maquina_passoapasso.run(fita, instrucoes, instrucao_inicial)
		except Exception as e:
			self.texto_resultado.setText('Erro: {}'.format(e))

	def gerar_instrucao(self, instrucoes):
		self.tabela.setRowCount(len(instrucoes) + 1)
		self.tabela.clearContents()
		cont = 0
		for instrucao in instrucoes:
			chave = instrucoes[instrucao]
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
		self.t_pause = False
		self.setWindowTitle('Executar')
		self.setMinimumWidth(800)
		self.fita = None
		self.instrucoes = None
		self.maquina = turingmachine.TuringMachine()
		self.tabela_fita = QTableWidget(2, 2)
		self.tabela_fita.horizontalHeader().hide()
		self.tabela_fita.setVerticalHeaderLabels(['Fita', 'Instrução'])
		self.tabela_fita.setStyleSheet('font: 12pt')
		self.botao_proximopasso = QPushButton('Próximo passo')
		self.botao_proximopasso.clicked.connect(self.proximo_passo)
		self.botao_passoapasso_1s = QPushButton('Resumir processo (1s/passo)')
		self.botao_passoapasso_1s.clicked.connect(self.passo_a_passo)
		self.botao_pausa = QPushButton('Pausar execução')
		self.botao_pausa.clicked.connect(self.pausa_passoapasso)
		self.caixa_execucao = QHBoxLayout()
		self.caixa_execucao.addWidget(self.botao_proximopasso)
		self.caixa_execucao.addWidget(self.botao_passoapasso_1s)
		self.caixa_execucao.addWidget(self.botao_pausa)
		self.texto_resultado = QLabel()
		self.texto_resultado.setStyleSheet('font: 14pt')
		layout = QVBoxLayout()
		layout.addWidget(self.tabela_fita)
		layout.addLayout(self.caixa_execucao)
		layout.addWidget(self.texto_resultado)
		self.setLayout(layout)

	def passo_a_passo(self):
		self.t = threading.Thread(target=self.passo_a_passo_thread)
		self.t_pause = False
		if self.t.isAlive():
			self.t.run()
		else:
			self.t.start()

	def passo_a_passo_thread(self):
		estado_atual = ''
		self.tempo = 1
		while estado_atual.upper() != 'END' and estado_atual.upper() != 'ERRO' and not self.t_pause:
			qt_app.processEvents()
			estado_atual = self.proximo_passo()
			time.sleep(self.tempo)

	def proximo_passo(self):
		try:
			fita, posicao_cabeca, estado_atual = self.maquina.operacao()
		except Exception as e:
			self.texto_resultado.setText('Erro: {}'.format(e))
			estado_atual = 'ERRO'
			return estado_atual
		self.gerar_tabela()
		self.atualizar_dados(1, posicao_cabeca, estado_atual)
		if estado_atual.upper() == 'END':
			self.botao_proximopasso.setDisabled
			self.botao_passoapasso_1s.setDisabled
		return estado_atual

	def pausa_passoapasso(self):
		self.t_pause = True

	def atualizar_dados(self, linha, coluna, info):
		self.tabela_fita.setItem(linha, coluna, QTableWidgetItem(info))
		self.tabela_fita.setColumnWidth(coluna, 2)

	def gerar_tabela(self):
		self.tabela_fita.clearContents()
		self.tabela_fita.setColumnCount(len(self.fita))
		for i in range(len(self.fita)):
			self.atualizar_dados(0, i, self.fita[i])

	def run(self, fita, instrucoes, instrucao_inicial):
		self.texto_resultado.clear()
		if not fita:
			raise Exception('Fita não detectada')
		self.fita = list(fita)
		self.instrucoes = instrucoes
		self.maquina.limpar_maquina()
		self.maquina.entrada_info(self.fita, self.instrucoes, instrucao_inicial)
		self.gerar_tabela()
		self.atualizar_dados(1, 0, instrucao_inicial)
		self.show()


Window().run()
