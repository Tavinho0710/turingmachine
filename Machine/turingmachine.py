class TuringMachine(object):
	def __init__(self):
		self.fita = None
		self.posicao_cabeca = 0
		self.instrucoes = None
		self.estado_atual = 'q0'
		self.leitura_cabeca = 0

	def start(self, fita, instrucoes):
		self.stringToList(fita)
		self.instrucoes = instrucoes
		self.leitura_cabeca = self.fita[0]
		while self.estado_atual!='END':
			chave = (self.estado_atual, self.leitura_cabeca)
			if chave in instrucoes:
				instrucao = instrucoes[chave]
				self.estado_atual = instrucao[0]
				self.fita[self.posicao_cabeca] = instrucao[1]
				if instrucao[2] == 'D':
					self.posicao_cabeca += 1
				elif instrucao[2] == 'E' and self.posicao_cabeca > 0:
					self.posicao_cabeca -= 1
				else:
					pass
				if self.posicao_cabeca == len(self.fita):
					self.fita.append(' ')
				self.leitura_cabeca = self.fita[self.posicao_cabeca]
			print(''.join(self.fita))
		return ''.join(self.fita)

	def stringToList(self, fita):
		self.fita = list(fita)
