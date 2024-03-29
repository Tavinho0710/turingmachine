class TuringMachine(object):
	def __init__(self):
		self.fita = None
		self.instrucoes = None
		self.leitura_cabeca = None
		self.estado_atual = ''
		self.posicao_cabeca = 0

	def entrada_info(self, fita, instrucoes, instrucao_inicial):
		self.limpar_maquina()
		self.instrucoes = instrucoes
		self.fita = fita
		self.estado_atual = instrucao_inicial
		self.leitura_cabeca = self.fita[0]

	def start(self):
		self.leitura_cabeca = self.fita[0]
		while self.estado_atual.upper() != 'END':
			self.operacao()
		while self.fita[0] == ' ':
			self.fita.pop(0)
		return ''.join(self.fita)

	def operacao(self):
		if self.estado_atual.upper() == 'END':
			return self.fita, self.posicao_cabeca, self.estado_atual
		chave = (self.estado_atual, self.leitura_cabeca)
		if chave in self.instrucoes:
			instrucao = self.instrucoes[chave]
			self.estado_atual = instrucao[0]
			self.fita[self.posicao_cabeca] = instrucao[1]
			if instrucao[2].upper() == 'D':
				self.posicao_cabeca += 1
			elif instrucao[2].upper() == 'E' and self.posicao_cabeca > 0:
				self.posicao_cabeca -= 1
			else:
				raise Exception('Direção indicada na instrução {0},{1} não foi reconhecida'.format(chave[0], chave[1]))
			if self.posicao_cabeca == len(self.fita):
				self.fita.append(' ')
			elif self.posicao_cabeca == 0:
				self.fita.insert(0, ' ')
				self.posicao_cabeca += 1
			self.leitura_cabeca = self.fita[self.posicao_cabeca]
		else:
			raise Exception('A operação {0} não foi encontrada na lista de instruções'.format(chave))
		return self.fita, self.posicao_cabeca, self.estado_atual

	def limpar_maquina(self):
		self.fita = None
		self.instrucoes = None
		self.estado_atual = ''
		self.posicao_cabeca = 0
		self.leitura_cabeca = 0
