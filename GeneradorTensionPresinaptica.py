#!/usr/bin/env python3
from definitions import *

class GeneradorTensionPresinaptica(object):
	def __init__(self, ambiente, entrada_neuronal, tiempo_de_inicio):
		self.ambiente=ambiente
		self.entrada_neuronal=entrada_neuronal
		# self.tiempo_actual=0.0
		# random_generator=np.random.default_rng()
		self.tension_excitatoria= ALFA_EXCITATORIO*math.exp(1)/(TAU_EXCITATORIO*CAPACITANCIA_MEMBRANA)
		self.tension_inhibitoria= ALFA_INHIBITORIO*math.exp(1)/(TAU_INHIBITORIO*CAPACITANCIA_MEMBRANA)
		self.random_generator=np.random.default_rng()
		self.indice_de_paso=0
		self.tiempo_de_inicio= tiempo_de_inicio
		self.recurso=simpy.Resource(self.ambiente, capacity=1)

	def realizar_arribos_excitatorios(self):
		tiempo_de_arribo_discreto=0
		while True:
			tiempo_de_arribo = self.random_generator.exponential(TASA_DE_ARRIBO_EXCITATORIO)
			yield self.ambiente.timeout(round(tiempo_de_arribo, 6))
			tension_temporal =[self.tension_excitatoria, time.time()-self.tiempo_de_inicio]
			yield self.entrada_neuronal.put(tension_temporal)

	def realizar_arribos_inhibitorios(self):
		tiempo_de_arribo_discreto=0
		while True:
			tiempo_de_arribo = self.random_generator.exponential(TASA_DE_ARRIBO_INHIBITORIO)
			yield self.ambiente.timeout(round(tiempo_de_arribo,6))
			tension_temporal =[self.tension_inhibitoria, time.time()-self.tiempo_de_inicio]
			yield self.entrada_neuronal.put(tension_temporal)

	def realizar_arribos_nulos(self):
		while True:
			yield self.ambiente.timeout(PASO)
			tension_temporal =[CORRIENTE_NULA, time.time()-self.tiempo_de_inicio]
			yield self.entrada_neuronal.put(tension_temporal)
