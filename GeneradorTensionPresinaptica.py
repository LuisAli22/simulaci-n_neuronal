#!/usr/bin/env python3
from definitions import *

class GeneradorTensionPresinaptica(object):
	def __init__(self, ambiente, entrada_neuronal):
		self.ambiente=ambiente
		self.entrada_neuronal=entrada_neuronal
		self.tension_excitatoria= ALFA_EXCITATORIO*math.exp(1)/(TAU_EXCITATORIO*CAPACITANCIA_MEMBRANA)
		self.tension_inhibitoria= ALFA_INHIBITORIO*math.exp(1)/(TAU_INHIBITORIO*CAPACITANCIA_MEMBRANA)
		self.random_generator=np.random.default_rng()

	def realizar_arribos_excitatorios(self):
		while True:
			tiempo_de_arribo = self.random_generator.exponential(TASA_DE_ARRIBO_EXCITATORIO)
			yield self.ambiente.timeout(round(tiempo_de_arribo, 6))
			yield self.entrada_neuronal.put(self.tension_excitatoria)

	def realizar_arribos_inhibitorios(self):
		while True:
			tiempo_de_arribo = self.random_generator.exponential(TASA_DE_ARRIBO_INHIBITORIO)
			yield self.ambiente.timeout(round(tiempo_de_arribo,6))
			yield self.entrada_neuronal.put(self.tension_inhibitoria)

#	def realizar_arribos_nulos(self):
#		while True:
#			yield self.ambiente.timeout(PASO)
#			yield self.entrada_neuronal.put(CORRIENTE_NULA)
