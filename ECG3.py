import wfdb
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Nombre del archivo del registro
ecg1 = 'a04'

try:
    # Leer el archivo del registro
    record = wfdb.rdrecord(ecg1)
except FileNotFoundError:
    print(f"Archivo '{ecg1}' no encontrado.")
    exit()

# Extraer la señal, etiquetas, frecuencia de muestreo y tiempo
senal = record.p_signal
etiquetas = record.sig_name
frecuencia = record.fs  # Frecuencia de muestreo
tiempo = np.arange(senal.shape[0]) / frecuencia  # Crear vector de tiempo

# Filtrar los primeros 10 segundos
duracion_segundos = 10
muestras_10s = int(frecuencia * duracion_segundos)  # Número de muestras en 10 segundos
senal_10s = senal[:muestras_10s]  # Cortar señal
tiempo_10s = tiempo[:muestras_10s]  # Cortar tiempo

# Información básica
print("Laboratorio 1: Análisis estadístico de la señal")
print(f"Frecuencia de muestreo: {frecuencia} Hz")
print(f"Forma completa de la señal: {senal.shape}")
print(f"Forma de la señal (10 segundos): {senal_10s.shape}")

# Graficar los primeros 10 segundos de la señal
plt.figure(figsize=(10, 5))
plt.title("Señal ECG - Primeros 10 segundos")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_10s, label='ECG Canal I', color='blue')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_10s) - 0.1, np.max(senal_10s) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

# FUNCIONES PARA CALCULAR ESTADISTICAS BASICAS
def calcular_media(datos):
    sumita=0
    for i in datos:
       sumita+= i
    return sumita/ len(datos)
       
def calcular_desviacion(datos, media):
    suma_v=0
    for i in datos:
        suma_v+=(i-media)**2
    varianza=suma_v/len(datos)
    return varianza ** 0.5

def calcular_coef_variacion(media, desviacion):
    return (desviacion / media) * 100

# Calcular y mostrar estadísticas manualmente
print("\nResultados calculados manualmente:")
for i, canal in enumerate(senal.T):  # Iterar por canal
    media_manual = calcular_media(canal)
    desviacion_manual = calcular_desviacion(canal, media_manual)
    coef_variacion_manual = calcular_coef_variacion(media_manual, desviacion_manual)
    
    print(f"Canal {etiquetas[i]}:")
    print(f"  Media: {media_manual:.3f}")
    print(f"  Desviación estándar: {desviacion_manual:.3f}")
    print(f"  Coeficiente de variación: {coef_variacion_manual:.2f}%")
    

# Calcular estadísticas usando numpy
media = np.mean(senal, axis=0)  # Media por canal
desviacion = np.std(senal, axis=0, ddof=1)  # Desviación estándar por canal
coef_variacion = (desviacion / media) * 100  # Coeficiente de variación (%)

print("\nResultados calculados con NumPy:")
for i, etiqueta in enumerate(etiquetas):
    print(f"Canal {etiqueta}:")
    print(f"  Media: {media[i]:.3f}")
    print(f"  Desviación estándar: {desviacion[i]:.3f}")
    print(f"  Coeficiente de variación: {coef_variacion[i]:.2f}%")

plt.show()
#Histograma
plt.figure(figsize=(10, 6))
sns.histplot(senal_10s, bins=60, color='blue', edgecolor='black', alpha=0.7, kde=True)
# Configurar el gráfico
plt.title('Histograma y Densidad de Probabilidad de la Señal ECG (Primeros 10 segundos)')
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad de Probabilidad')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# RUIDO GAUSSIANO (SNR MENOR A 10dB)
P_signal = np.mean(senal_10s**2)  # Potencia de la señal original
r_gaussiano1 = np.random.normal(0, 1, muestras_10s) #el 0 representa la media, el 1 la desviación
P_noise_white = np.mean(r_gaussiano1**2)  # Potencia del ruido
r_gaussiano1*=0.1397 # ajustar potencia del ruido para un SNR bajo
senal_noise_white1 = senal_10s + r_gaussiano1  # Señal con ruido
SNR_noise_white1 = 10 * np.log10(P_signal / np.mean(r_gaussiano1**2))  # Cálculo del SNR real
# RUIDO GAUSSIANO (SNR MAYOR A 10dB)
r_gaussiano2 = np.random.normal(0, 1, muestras_10s)
r_gaussiano2*=0.00982
senal_noise_white2 = senal_10s + r_gaussiano2  # Señal con ruido
SNR_noise_white2 = 10 * np.log10(P_signal / np.mean(r_gaussiano2**2))  # Cálculo del SNR real
print("RUIDO TIPO GAUSSIANO")
print(f"SNR menor a 10db: {SNR_noise_white1:.2f} dB")
print(f"SNR mayor a 10db: {SNR_noise_white2:.2f} dB")
# Tercera figura con dos señales de ruido blanco
fig3, axs3 = plt.subplots(2, 1, figsize=(12, 7))
plt.subplots_adjust(hspace=0.4)

axs3[0].plot(tiempo_10s, senal_noise_white1, color='orange')
axs3[0].set_title("Señal con Ruido Blanco 1")
axs3[0].set_xlabel("Tiempo (s)")
axs3[0].set_ylabel("Amplitud (mV)")
axs3[0].grid(True, linestyle="--", alpha=0.7)

axs3[1].plot(tiempo_10s, senal_noise_white2, color='brown')
axs3[1].set_title("Señal con Ruido Blanco 2")
axs3[1].set_xlabel("Tiempo (s)")
axs3[1].set_ylabel("Amplitud (mV)")
axs3[1].grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()

# Parámetros del ruido de artefacto
frecuencia_artefacto = 20  # Frecuencia del artefacto en Hz
amplitud_artefacto = 0.48 # Amplitud del artefacto

# ARTEFACTO
#--- PRIMER RUIDO ( SNR MENOR A 10 dB)
artefacto = amplitud_artefacto * np.sin(2 * np.pi * frecuencia_artefacto * tiempo_10s)

# Agregar el artefacto a la señal original
artefacto1 = artefacto.reshape(-1, 1)
senal_artefacto1 = senal_10s + artefacto1

# Cálculo del SNR
P_noise1 = np.mean(artefacto1**2)
SNR_1 = 15 * np.log10(P_signal / P_noise1)

# Graficar la señal con ruido de artefacto
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido de Artefacto")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_artefacto1, label='ECG con ruido de artefacto', color='purple')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_artefacto1) - 0.1, np.max(senal_artefacto1) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

# --- SEGUNDO RUIDO ( SNR MAYOR A 10 dB) ---
artefacto = 0.1* np.sin(2 * np.pi * 60 * tiempo_10s)

# Agregar el artefacto a la señal original
artefacto2 = artefacto.reshape(-1, 1)
senal_artefacto2 = senal_10s + artefacto2

# Cálculo del SNR
P_noise2 = np.mean(artefacto2**2)
SNR_2 = 10 * np.log10(P_signal / P_noise2)

# Graficar la señal con ruido de artefacto
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido de Artefacto 2")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_artefacto2, label='ECG con ruido de artefacto', color='green')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_artefacto2) - 0.1, np.max(senal_artefacto2) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

# Imprimir los valores de SNR
print("RUIDO TIPO ARTEFACTO")
print(f"SNR menor a 10dB: {SNR_1:.2f} dB")
print(f"SNR mayor a 10dB: {SNR_2:.2f} dB")

#Extraer la señal, etiquetas, frecuencia de muestreo y tiempo
senal = record.p_signal
etiquetas = record.sig_name
frecuencia = record.fs  # Frecuencia de muestreo
tiempo = np.arange(senal.shape[0]) / frecuencia  # Crear vector de tiempo

# Filtrar los primeros 10 segundos, convertir las muestras a tiempo
duracion_segundos = 10
muestras_10s = int(frecuencia * duracion_segundos)  # Número de muestras en 10 segundos
senal_10s = senal[:muestras_10s, :]  # Cortar señal
tiempo_10s = tiempo[:muestras_10s]  # Cortar tiempo

#RUIDO IMPULSO (SNR MENOR A 10 dB)
ruido_impulso_bajo = np.zeros_like(senal_10s) 
num_impulsos_bajo = 10
posiciones_bajo = np.random.randint(0, muestras_10s, num_impulsos_bajo)

for pos in posiciones_bajo:
    amplitud_impulso_bajo = np.random.uniform(-3, 3, size=(senal_10s.shape[1],))  #Amplitud aleatorea entre -3 y 3mV
    ruido_impulso_bajo[pos, :] = amplitud_impulso_bajo

senal_con_impulso_bajo = senal_10s + ruido_impulso_bajo #suma del impulso a la original :)

P_signal = np.mean(senal_10s**2)#calculo de potencia
P_noise_impulso_bajo = np.mean(ruido_impulso_bajo**2)
SNR_impulso_bajo = 10 * np.log10(P_signal / P_noise_impulso_bajo)#conversion a decibeles

# RUIDO IMPULSO (SNR MAYOR A 10 dB)  
ruido_impulso_alto = np.zeros_like(senal_10s)
num_impulsos_alto = 10
posiciones_alto = np.random.randint(0, muestras_10s, num_impulsos_alto)

for pos in posiciones_alto: #lo mismo pero cambia el rango de la amplitud
    amplitud_impulso_alto = np.random.uniform(-0.1, 0.1, size=(senal_10s.shape[1],))  # Amplitud por canal
    ruido_impulso_alto[pos, :] = amplitud_impulso_alto

senal_con_impulso_alto = senal_10s + ruido_impulso_alto

P_noise_impulso_alto = np.mean(ruido_impulso_alto**2)
SNR_impulso_alto = 10 * np.log10(P_signal / P_noise_impulso_alto)

# Graficar las señales con ruido impulso
fig, axs = plt.subplots(2, 1, figsize=(12, 8))

axs[0].plot(tiempo_10s, senal_con_impulso_bajo[:, 0], label=f'Ruido Impulso (SNR bajo: {SNR_impulso_bajo:.2f} dB)', color='red')
axs[0].set_title("Señal ECG con Ruido Impulso - SNR Bajo")
axs[0].set_xlabel("Tiempo(s)")
axs[0].set_ylabel("Amplitud(mV)")
axs[0].legend()
axs[0].grid(True, linestyle="--", alpha=0.7)

axs[1].plot(tiempo_10s, senal_con_impulso_alto[:, 0], label=f'Ruido Impulso (SNR alto: {SNR_impulso_alto:.2f} dB)', color='blue')
axs[1].set_title("Señal ECG con Ruido Impulso - SNR Alto")
axs[1].set_xlabel("Tiempo(s)")
axs[1].set_ylabel("Amplitud(mV)")
axs[1].legend()
axs[1].grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()

# Mostrar valores de SNR
print("RUIDO TIPO IMPULSO")
print(f"SNR menor a 10 dB: {SNR_impulso_bajo:.2f} dB")
print(f"SNR mayor a 10 dB: {SNR_impulso_alto:.2f} dB")