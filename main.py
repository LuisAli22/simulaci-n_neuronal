#!/usr/bin/env python3

import matplotlib.pyplot as plt
from definitions import*
from GeneradorTensionPresinaptica import *
from Neurona import *


if __name__ == '__main__':
	start_time = time.time()
	ambiente = simpy.Environment()
	entrada_neuronal = simpy.Store(ambiente)
	tension_de_salida=[]
	tiempo=[]
	neurona= Neurona(ambiente, entrada_neuronal)
	generador_tension_presinaptica =GeneradorTensionPresinaptica(ambiente, entrada_neuronal, start_time)
	ambiente.process(neurona.run(tension_de_salida, start_time, tiempo))
	ambiente.process(generador_tension_presinaptica.realizar_arribos_excitatorios())
	ambiente.process(generador_tension_presinaptica.realizar_arribos_inhibitorios())
	#ambiente.process(generador_tension_presinaptica.realizar_arribos_nulos())
	ambiente.run(until=0.2)
	print("--- %s seconds ---" % (time.time() - start_time))
	plt.plot(tiempo, tension_de_salida)
	plt.show()
	# Y_k=np.zeros(3)
	# A=np.array([[-1/TAU_ALFA, 0, 0],
	# 			[1, -1/TAU_ALFA, 0],
	# 			[0, 1, -1/TAU_MEMBRANA]])
	# matriz_exponencial= construir_matriz_exponencial()
	# tiempo_actual=0
	# output=np.array([])
	# while  tiempo_actual < TIEMPO_TOTAL_SIMULACION:
	# 	input=np.array([corriente_de_entrada.obtener(tiempo_actual/PASO), 0, 0])
	# 	#input=np.array(s[start:start+3])
	# 	Y_k_siguiente=matriz_exponencial.dot(Y_k)+input
	# 	output= np.append(output, Y_k_siguiente[-1])
	# 	Y_k=Y_k_siguiente
	# 	tiempo_actual+=PASO
	# print(output)
	# plt.stem(output)
	# plt.show()
