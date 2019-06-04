import json
import socket
import sys
import time
from threading import Thread

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QApplication

import turingmachine

qt_app = QApplication(sys.argv)


class Executar(QWidget):
	def __init__(self):
		# TODO: Histórico de instruções
		# TODO: Botões de velocidade e pausa da thread

		QWidget.__init__(self)
		self.setWindowTitle('Executar')
		self.setMinimumWidth(800)
		self.fita = None
		self.instrucoes = None
		self.maquina = turingmachine.TuringMachine()
		self.tabela_fita = QTableWidget(2, 2)
		self.tabela_fita.horizontalHeader().hide()
		self.tabela_fita.verticalHeader().hide()
		self.tabela_fita.setStyleSheet('font: 12pt')
		self.botao_proximopasso = QPushButton('Próximo passo')
		self.botao_proximopasso.clicked.connect(self.proximo_passo)
		self.botao_passoapasso_1s = QPushButton('Resumir processo (1s/passo)')
		self.botao_passoapasso_1s.clicked.connect(self.passo_a_passo)
		self.caixa_execucao = QHBoxLayout()
		self.caixa_execucao.addWidget(self.botao_proximopasso)
		self.caixa_execucao.addWidget(self.botao_passoapasso_1s)
		layout = QVBoxLayout()
		layout.addWidget(self.tabela_fita)
		layout.addLayout(self.caixa_execucao)
		self.setLayout(layout)

	def passo_a_passo(self):
		self.t = Thread(target=self.passo_a_passo_thread)
		if self.t.isAlive():
			pass
		else:
			self.t.start()

	def passo_a_passo_thread(self):
		estado_atual = None
		while estado_atual != 'END':
			qt_app.processEvents()
			estado_atual = self.proximo_passo()
			time.sleep(0.5)

	def proximo_passo(self):
		fita, posicao_cabeca, estado_atual = self.maquina.operacao()
		self.gerar_tabela()
		self.atualizar_dados(1, posicao_cabeca, estado_atual)
		if estado_atual == 'END':
			self.botao_proximopasso.setDisabled
			self.botao_passoapasso_1s.setDisabled
		return estado_atual

	def atualizar_dados(self, linha, coluna, info):
		self.tabela_fita.setItem(linha, coluna, QTableWidgetItem(info))
		self.tabela_fita.setColumnWidth(coluna, 2)

	def gerar_tabela(self):
		self.tabela_fita.clearContents()
		self.tabela_fita.setColumnCount(len(self.fita))
		for i in range(len(self.fita)):
			self.atualizar_dados(0, i, self.fita[i])

	def run(self):
		qt_app.exec_()
		host, porta = 'localhost', 8888
		cliente = None
		while True:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao:
				conexao.bind(host, porta)
				conexao.listen(1)
				conn, cliente = conexao.accept()
				data = conn.recv(16384)
				self.fita, self.instrucoes, instrucao_inicial = json.loads(data)
				conn.close()
			self.maquina.limpar_maquina()
			self.maquina.entrada_info(self.fita, self.instrucoes, instrucao_inicial)
			self.gerar_tabela()
			self.atualizar_dados(1, 0, instrucao_inicial)
			self.show()


Executar.run()
