import soma
from Machine.turingmachine import TuringMachine

fita = input("Insira fita aqui")

maquina = TuringMachine()
resultado = maquina.start(fita, soma.instrucoes)
print(resultado)
