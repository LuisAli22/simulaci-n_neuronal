#!/usr/bin/env python3

import matplotlib.pyplot as plt
from definitions import*

def PSC(tiempo, alfa, tau):
	k=(ALFA_EXCITATORIO/TAU_EXCITATORIO)
	if tiempo<0:
		return 0.0
	return k*tiempo*math.exp(1-(tiempo/TAU_EXCITATORIO))
def tiempos_de_arribo(tasa_de_arribo):
	tiempo_total= 0.2
	random_generator=np.random.default_rng()
	tiempo_arribo=random_generator.exponential(TASA_DE_ARRIBO_EXCITATORIO)
	indice_arribo=int(round(tiempo_arribo,6)/PASO)
	indice=0.0
	for time in np.arange(0.0,0.2,PASO):
		if indice==indice_arribo:
			yield time
			tiempo_arribo=random_generator.exponential(TASA_DE_ARRIBO_EXCITATORIO)
			indice_arribo=int(round(tiempo_arribo,6)/1e-6)+indice
		indice +=1.0

if __name__ == '__main__':
	tiempos_de_arribo_excitatorios=tiempos_de_arribo(TASA_DE_ARRIBO_EXCITATORIO)
	tiempos_de_arribo_inhibitorios=tiempos_de_arribo(TASA_DE_ARRIBO_INHIBITORIO)
	t=PASO*100000
	cumsum=0
	for tiempo_excitatorio in tiempos_de_arribo_excitatorios:
		cumsum+=PSC(t-tiempo_excitatorio, ALFA_EXCITATORIO, TAU_EXCITATORIO)
	for tiempo_inhibitorio in tiempos_de_arribo_inhibitorios:
		cumsum+=PSC(t-tiempo_inhibitorio, ALFA_INHIBITORIO, TAU_INHIBITORIO)
	print("I(",t,")= ",cumsum)