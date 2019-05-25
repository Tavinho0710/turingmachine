import instrucoes
from Machine.turingmachine import TuringMachine

fita = input("Insira fita aqui")

maquina = TuringMachine()
resultado = maquina.start(fita, instrucoes.multiplicacao)
print(resultado)