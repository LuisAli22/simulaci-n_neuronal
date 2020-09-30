#!/usr/bin/env python3

import matplotlib.pyplot as plt
from definitions import*

def PSC(tiempo, alfa, tau):
	k=(alfa/tau)
	if tiempo>=0:
		return k*tiempo*math.exp(1-(tiempo/tau))
	return 0.0
def tiempos_de_arribo(tasa_de_arribo, tiempos_de_arribo):
	tiempo_total= DURACION
	random_generator=np.random.default_rng()
	tiempo_actual=0
	while tiempo_actual <= DURACION:
		tiempo_de_ocurrencia= random_generator.exponential(tasa_de_arribo)
		tiempo_actual+=tiempo_de_ocurrencia
		if tiempo_actual <= DURACION:
			tiempos_de_arribo.append(tiempo_actual)

def corriente(t, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios):
	cumsum=0
	for tiempo_excitatorio in tiempos_de_arribo_excitatorios:
		cumsum+=PSC(t-tiempo_excitatorio, ALFA_EXCITATORIO, TAU_EXCITATORIO)
	for tiempo_inhibitorio in tiempos_de_arribo_inhibitorios:
		cumsum+=PSC(t-tiempo_inhibitorio, ALFA_INHIBITORIO, TAU_INHIBITORIO)
	return cumsum

def integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios):
	return ((POTENCIAL_DE_REPOSO-v)/TAU_MEMBRANA)+(corriente(t,tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios)/CAPACITANCIA_MEMBRANA)

def regimen_estacionario(t, v, inicio_tiempo_refractario):
	return 0.0

def umbral_alcanzado(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios):
	return TENSION_UMBRAL - v[0]

def fin_periodo_refractario(t, v, inicio_tiempo_refractario):
	return t - inicio_tiempo_refractario - TIEMPO_REFRACTARIO

evento_fin_periodo_refractario = lambda t,v:fin_periodo_refractario(t,v, inicio_tiempo_refractario)
evento_fin_periodo_refractario.terminal = True
evento_fin_periodo_refractario.direction = 1
evento_umbral = lambda t,v:umbral_alcanzado(t,v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios)
evento_umbral.terminal = True
evento_umbral.direction = -1

def esta_en_periodo_refractario(inicio_tiempo_refractario):
	return (inicio_tiempo_refractario!=0)

if __name__ == '__main__':
	tiempos_de_arribo_excitatorios=[]
	tiempos_de_arribo_inhibitorios=[]
	tiempos_de_arribo(TASA_DE_ARRIBO_EXCITATORIO, tiempos_de_arribo_excitatorios)
	tiempos_de_arribo(TASA_DE_ARRIBO_INHIBITORIO, tiempos_de_arribo_inhibitorios)
	ts=[]
	ys=[]
	t_inicio=0
	inicio_tiempo_refractario=0
	
	while True:
		if esta_en_periodo_refractario(inicio_tiempo_refractario):
			r=solve_ivp(fun=lambda t, v: regimen_estacionario(t, v, inicio_tiempo_refractario), t_span=[t_inicio, DURACION], y0=[POTENCIAL_DE_REPOSO], events= evento_fin_periodo_refractario, max_step=0.01, dense_output=True)
			t = np.linspace(t_inicio, r.t[-1], 500)
			z=r.sol(t)
			ts.append(t)
			ys.append(z)
			if r.status == 1:
				t_inicio = r.t[-1]
				v = r.y[:, -1].copy()
				inicio_tiempo_refractario= 0
			else:
				break
		else:
			r=solve_ivp(fun=lambda t, v: integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios), t_span=[t_inicio, DURACION], y0=[POTENCIAL_DE_REPOSO], events= evento_umbral, max_step=0.01, dense_output=True)
			t = np.linspace(t_inicio, r.t[-1], 500)
			z=r.sol(t)
			ts.append(t)
			ys.append(z)
			if r.status == 1: 
				t_inicio = r.t[-1]
				v = r.y[:, -1].copy()
				inicio_tiempo_refractario= t_inicio
			else:
				break

	t = np.linspace(0, DURACION, 500)
	
	r=solve_ivp(fun=lambda t, v: integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios), t_span=[0, DURACION], y0=[POTENCIAL_DE_REPOSO], dense_output=True)
	z = r.sol(t)
	plt.subplot(211)
	plt.plot(np.concatenate(ts), np.concatenate(ys, axis=1).T*1000)
	plt.ylabel("Potencial (mv)")
	plt.title('Integrate and fire con umbral')
	plt.grid(True)

	plt.subplot(212)
	plt.plot(t, z.T*1000)
	plt.ylabel("Potencial (mv)")
	plt.title('Integrate and fire sin umbral ')
	plt.grid(True)
	plt.show()
