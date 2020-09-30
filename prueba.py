#!/usr/bin/env python3

import matplotlib.pyplot as plt
from definitions import*
DURACION= 0.2
tensiones_de_salida= []
fin_regimen_diferencial=False

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
	#tiempo_arribo=random_generator.exponential(tasa_de_arribo)
	#indice_arribo=int(round(tiempo_arribo,6)/PASO)
	#indice=0.0
	#for time in np.arange(0.0,DURACION,PASO):
	#	if indice==indice_arribo:
	#		yield time
	#		tiempo_arribo=random_generator.exponential(tasa_de_arribo)
	#		indice_arribo=int(round(tiempo_arribo,6)/1e-6)+indice
	#	indice +=1.0
def corriente(t, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios):
	cumsum=0
	for tiempo_excitatorio in tiempos_de_arribo_excitatorios:
		#print("excitatorio: ",t-tiempo_excitatorio)
		cumsum+=PSC(t-tiempo_excitatorio, ALFA_EXCITATORIO, TAU_EXCITATORIO)
	for tiempo_inhibitorio in tiempos_de_arribo_inhibitorios:
		#print("inhibitorio: ",t-tiempo_inhibitorio)
		cumsum+=PSC(t-tiempo_inhibitorio, ALFA_INHIBITORIO, TAU_INHIBITORIO)
	#print("I(",t,")= ",cumsum)
	return cumsum
def integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios):
	#print("Aca entra!")
	return ((POTENCIAL_DE_REPOSO-v)/TAU_MEMBRANA)+(corriente(t,tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios)/CAPACITANCIA_MEMBRANA)

def regimen_estacionario(t, v, inicio_tiempo_refractario):
	return 0.0


def solout(t, y):
	tensiones_de_salida.append([t, *y])
	return 0

def umbral_alcanzado(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios):
	print("Tension que supera al umbral ", v[0])
	return TENSION_UMBRAL - v[0]

def fin_periodo_refractario(t, v, inicio_tiempo_refractario):
	#print(t - inicio_tiempo_refractario - TIEMPO_REFRACTARIO)
	return t - inicio_tiempo_refractario - TIEMPO_REFRACTARIO

evento_fin_periodo_refractario = lambda t,v:fin_periodo_refractario(t,v, inicio_tiempo_refractario)
evento_fin_periodo_refractario.terminal = True
evento_fin_periodo_refractario.direction = 1

#umbral_alcanzado.terminal=True
#umbral_alcanzado.direction= 1
evento_umbral = lambda t,v:umbral_alcanzado(t,v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios)
evento_umbral.terminal = True
evento_umbral.direction = -1
#def obtener_tension_salida():
	#tiempos_de_arribo_excitatorios=[]
	#tiempos_de_arribo_inhibitorios=[]
	#tiempos_de_arribo(TASA_DE_ARRIBO_EXCITATORIO, tiempos_de_arribo_excitatorios)
	#tiempos_de_arribo(TASA_DE_ARRIBO_INHIBITORIO, tiempos_de_arribo_inhibitorios)
	#t=0
	#print("I(",t,")= ", corriente(t, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios))
	#tiempo = PASO
	#v0=POTENCIAL_DE_REPOSO
	#r=ode(f).set_integrator('dopri5')
	#r=solve_ivp(integrate_and_fire,[0, DURACION], POTENCIAL_DE_REPOSO, events= umbral_alcanzado)
	#r.set_initial_value(v0).set_f_params(tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios)
	#r.set_solout(solout)
	#r.integrate(DURACION)
	#r.t=PASO
	#if r.successful:
	#	print(r.integrate(tiempo[1]))
	#k=1
	#print(tiempo)
	#tension_actual=POTENCIAL_DE_REPOSO
	#tiempo_actual=0
	#while r.successful() and r.t < DURACION and not fin_regimen_diferencial:
		#print(r.t)
	#	r.integrate(r.t+PASO)
		#print(tension_actual)
		#if tension_actual>= TENSION_UMBRAL:
		#	print("Se supera el umbral, ", tension_actual)
		#tiempo_actual=r.t+PASO
		#tensiones_de_salida.append(tension[0])
		#if tension_actual>= TENSION_UMBRAL:
		#	print("Se supera el umbral")
		#	r.set_initial_value(v0, tiempo_actual).set_f_params(tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios)
def esta_en_periodo_refractario(inicio_tiempo_refractario):
	return (inicio_tiempo_refractario!=0)

if __name__ == '__main__':
	tiempos_de_arribo_excitatorios=[]
	tiempos_de_arribo_inhibitorios=[]
	tiempos_de_arribo(TASA_DE_ARRIBO_EXCITATORIO, tiempos_de_arribo_excitatorios)
	tiempos_de_arribo(TASA_DE_ARRIBO_INHIBITORIO, tiempos_de_arribo_inhibitorios)
	ts=[]
	ys=[]
	t=0
	inicio_tiempo_refractario=0
	while True:
	    #sol = solve_ivp(fun, (t, tend), u, events=event)
		if esta_en_periodo_refractario(inicio_tiempo_refractario):
			print("Entro en periodo refractario")
			r=solve_ivp(fun=lambda t, v: regimen_estacionario(t, v, inicio_tiempo_refractario), t_span=[t, DURACION], y0=[POTENCIAL_DE_REPOSO], events= evento_fin_periodo_refractario, max_step=0.01)
			ts.append(r.t)
			ys.append(r.y)
			if r.status == 1: # Event was hit
				# New start time for integration
				#print("Se termino el periodo refractario")
				t = r.t[-1]
				# Reset initial state
				v = r.y[:, -1].copy()
				#v[0] = POTENCIAL_DE_REPOSO
				inicio_tiempo_refractario= 0
			else:
				break
		else:
			r=solve_ivp(fun=lambda t, v: integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios), t_span=[t, DURACION], y0=[POTENCIAL_DE_REPOSO], events= evento_umbral, max_step=0.01)
			ts.append(r.t)
			ys.append(r.y)
			if r.status == 1: # Event was hit
				# New start time for integration
				#print("Se alcanzo el limite")
				t = r.t[-1]
				# Reset initial state
				v = r.y[:, -1].copy()
				#v[0] = POTENCIAL_DE_REPOSO
				inicio_tiempo_refractario= t
			else:
				break
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	# We have to stitch together the separate simulation results for plotting
	ax.plot(np.concatenate(ts), np.concatenate(ys, axis=1).T)
	myleg = plt.legend(['v','u'])
	plt.show()
	#t = np.linspace(0, DURACION, 500)
	#r=solve_ivp(fun=lambda t, v: integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios), t_span=[0, DURACION], y0=[POTENCIAL_DE_REPOSO], events= evento_umbral, max_step=0.01)
	#print(t)
	#z = r.sol(t)
	#plt.plot(tensiones_de_salida[:,0], tensiones_de_salida[:,1], 'b.-')
	#print(r.t)
	#print(r.y)
	#plt.plot(t, z.T)
	#print(r.t_events[0])
	#plt.plot(r.t,r.y[0], linewidth=3)
	#plt.show()
#	plt.plot(tensiones_de_salida)
#	plt.show()
