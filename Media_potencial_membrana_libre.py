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
	tiempo_actual=0.0
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

def integral_PSP(alfa, tau):
	return (alfa*tau*math.exp(1)*(TAU_MEMBRANA/CAPACITANCIA_MEMBRANA))

def integral_PSP_cuadrado(alfa, tau):
	numerador=alfa*tau*math.exp(1)*TAU_MEMBRANA
	denominador= 2*CAPACITANCIA_MEMBRANA*(TAU_MEMBRANA+tau)
	return (((2*TAU_MEMBRANA)+tau)*((numerador/denominador)**2))

def obtener_lambda_inhibitorio(media, lambda_excitatorio):
	cociente_de_integrales=(integral_PSP(ALFA_EXCITATORIO, TAU_EXCITATORIO)/integral_PSP(ALFA_INHIBITORIO, TAU_INHIBITORIO))
	cociente_diferencia_potencial_integral= ((POTENCIAL_DE_REPOSO- media)/integral_PSP(ALFA_INHIBITORIO, TAU_INHIBITORIO))
	return (((-1)*cociente_de_integrales*lambda_excitatorio) - cociente_diferencia_potencial_integral)
def media_teorica(lambda_excitatorio, lambda_inhibitorio):
	return (POTENCIAL_DE_REPOSO + (lambda_excitatorio*integral_PSP(ALFA_EXCITATORIO, TAU_EXCITATORIO)) + (lambda_inhibitorio*integral_PSP(ALFA_INHIBITORIO, TAU_INHIBITORIO)))
def desvio_teorico(lambda_excitatorio, lambda_inhibitorio):
	return math.sqrt((lambda_excitatorio*integral_PSP_cuadrado(ALFA_EXCITATORIO, TAU_EXCITATORIO)) + (lambda_inhibitorio*integral_PSP_cuadrado(ALFA_INHIBITORIO, TAU_INHIBITORIO)))

if __name__ == '__main__':
	media= media_teorica(LAMBDA_EXCITATORIO, LAMBDA_INHIBITORIO)
	todas_las_medias=[]
	todos_los_desvios=[]
	todas_las_medias_teoricas=[]
	todos_los_desvios_teoricos=[]
	lambda_excitatorio=LAMBDA_EXCITATORIO
	lambdas_excitatorios=[]
	print("Simulando. Por favor, espere...")
	while lambda_excitatorio <=4000:	
		t = np.linspace(0, DURACION, 500)
		lambda_inhibitorio=round(obtener_lambda_inhibitorio(media, lambda_excitatorio), 0)
		tiempos_de_arribo_excitatorios=[]
		tiempos_de_arribo_inhibitorios=[]
		tiempos_de_arribo(1/lambda_excitatorio, tiempos_de_arribo_excitatorios)
		tiempos_de_arribo(1/lambda_inhibitorio, tiempos_de_arribo_inhibitorios)
		r=solve_ivp(fun=lambda t, v: integrate_and_fire(t, v, tiempos_de_arribo_excitatorios, tiempos_de_arribo_inhibitorios), t_span=[0, DURACION], y0=[POTENCIAL_DE_REPOSO], dense_output=True)
		z = r.sol(t)
		tensiones=np.array([tension for tension in z.T[:,0]])
		todas_las_medias.append(statistics.mean(z.T[:,0])*1000)
		todos_los_desvios.append(statistics.stdev(z.T[:,0])*1000)
		todas_las_medias_teoricas.append(media_teorica(lambda_excitatorio, lambda_inhibitorio)*1000)
		todos_los_desvios_teoricos.append(desvio_teorico(lambda_excitatorio, lambda_inhibitorio)*1000)
		lambdas_excitatorios.append(lambda_excitatorio)
		lambda_excitatorio+=100.0

	plt.subplot(211)
	plt.scatter(lambdas_excitatorios, todas_las_medias)
	plt.scatter(lambdas_excitatorios, todas_las_medias_teoricas)
	plt.ylabel("Media del Potencial (mv)")
	plt.title('Media')
	plt.grid(True)

	plt.subplot(212)
	plt.scatter(lambdas_excitatorios, todos_los_desvios)
	plt.scatter(lambdas_excitatorios, todos_los_desvios_teoricos)
	plt.ylabel("Desvío estandar del Potencial (mv)")
	plt.title('Media')
	plt.grid(True)
	plt.show()

