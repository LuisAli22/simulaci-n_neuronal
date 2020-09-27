#!/usr/bin/env python3
from definitions import *

class Neurona(object):
	def __init__(self, ambiente, entrada_neuronal):
		self.ambiente=ambiente
		self.entrada_neuronal=entrada_neuronal
		self.Y_k=np.array([0, 0, POTENCIAL_DE_REPOSO])
		self.matriz_exponencial_excitatoria= self.construir_matriz_exponencial(TAU_EXCITATORIO)
		self.matriz_exponencial_inhibitoria= self.construir_matriz_exponencial(TAU_INHIBITORIO)
		self.inicio_tiempo_refractario=0

	def construir_matriz_exponencial(self, tau):
		coef_11=coef_22=np.exp(-PASO/tau)
		coef_21=PASO*np.exp(-PASO/tau)
		coef_33= np.exp(-PASO/TAU_MEMBRANA)
		divisor=((1/tau)-(1/TAU_MEMBRANA))
		numerador=(coef_33 - coef_11)
		coef_31=(numerador/divisor**2) - (coef_21/divisor)
		coef_32=numerador/divisor
		return np.array([	[coef_11, 0, 0],
							[coef_21, coef_22, 0],
							[coef_31, coef_32,coef_33]])

	def es_tension_excitatiora(self, tension):
		return ((tension*(TAU_EXCITATORIO*CAPACITANCIA_MEMBRANA)/math.exp(1)) == ALFA_EXCITATORIO)

	def obtener_siguiente_estado(self, tension):
		input=np.array([tension, 0, 0])
		if self.es_tension_excitatiora(tension):
			return self.matriz_exponencial_excitatoria.dot(self.Y_k)+input
		return self.matriz_exponencial_inhibitoria.dot(self.Y_k)+input

	def esta_en_periodo_refractario(self):
		if self.inicio_tiempo_refractario == 0 :
			return False
		return (time.time() - self.inicio_tiempo_refractario <= TIEMPO_REFRACTARIO)

	def run(self, tension_de_salida):
		#tension_de_salida=0
		while True:
			tension_presinaptica = yield self.entrada_neuronal.get()
			if self.esta_en_periodo_refractario():
				self.Y_k=np.array([0, 0, POTENCIAL_DE_REPOSO])
			Y_k_siguiente= self.obtener_siguiente_estado(tension_presinaptica)
			tension_de_salida.append(Y_k_siguiente[-1])
			if Y_k_siguiente[-1] >= TENSION_UMBRAL:
				#print("Tension ", tension_de_salida[-1]," supera al umbral ",TENSION_UMBRAL)
				self.Y_k=np.array([0, 0, POTENCIAL_DE_REPOSO])
				self.inicio_tiempo_refractario = time.time()

			else:
				#print("Tension ", tension_de_salida[-1]," NO supera al umbral ")
				self.Y_k=Y_k_siguiente
