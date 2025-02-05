# Análisis estadístico de un ECG
## Descripción
El presente proyecto implementa el procesamiento y análisis estadístico de señales de ECG, abarcando la caracterización de parámetros estadísticos, la simulación de ruido en distintas configuraciones y la evaluación de la variabilidad de la señal en función de métricas cuantitativas.
> [!TIP]
>Librerias necesarias:
>```
> import wfdb
>import seaborn as sns
>import matplotlib.pyplot as plt
>import numpy as np
> ```
## Señal ECG
La señal utilizada fue extraída de Physionet de la base de datos Apnea-ECG Database, esta base de datos consiste en 70 grabaciones de larga duración (entre 7 y 10 horas) para investigar la apnea del sueño a través de señales de ECG. Cada grabación incluye una señal de ECG de 100 muestras por segundo. 
Se utilizó en a04.hea y el a04.dat, el .hea es un archivo de texto que describe el contenido de .dat, este tiene información como el número de señales, la frecuencia de muestreo, el formato de los datos y la escala de conversión de los valores digitales a unidades fisiológicas.

Link de Apnea-ECG Database: https://physionet.org/content/apnea-ecg/1.0.0/

Estos archivos se cargan en una IDE para Python y se utilizó la librería wfdb (Waveform Database), la cual es utilizada para visualizar señales fisiológicas, como los ECG.

```
#Extraer la señal, etiquetas, frecuencia de muestreo y tiempo
senal = record.p_signal
etiquetas = record.sig_name
frecuencia = record.fs  #Frecuencia de muestreo
tiempo = np.arange(senal.shape[0]) / frecuencia  #Crear vector de tiempo

```

Finalmente se trabajó con los primeros diez segundos para poder visualizar mejor la señal con los diferentes ruidos, así como reducir el uso de memoria y almacenamiento ya que la señal original tiene una duración de más de 7 horas.


```
#Filtrar los primeros 10 segundos, convertir las muestras a tiempo
duracion_segundos =10
muestras_10s = int(frecuencia * duracion_segundos)  #Número de muestras en 10 segundos
senal_10s = senal[:muestras_10s, :]  # Cortar señal
tiempo_10s = tiempo[:muestras_10s]  # Cortar tiempo
```
>[!TIP]
>Es preferible mostrar solo los primeros 10 segundos de la señal ECG para que la visualización sea más clara y fácil de analizar.

La señal obtenida representa es un registro de la actividad eléctrica del corazón a lo largo 10 segundos, siendo esta la de una persona con apnea del sueño, con una frecuencia de muestreo de  100Hz.

![image](https://github.com/user-attachments/assets/9565a6eb-8467-40c1-b40c-befab731b9b3)

                               
## Estadísticos descriptivos (Forma larga)
Se han implementado cálculos manuales para la media, desviación estándar y coeficiente de variación para verificar el comportamiento de la señal sin depender de bibliotecas especializadas. La media aritmética se obtiene sumando todos los valores y dividiendo entre el número total de muestras, proporcionando una medida central. La desviación estándar mide la dispersión de los datos respecto a la media, y el coeficiente de variación, expresado en porcentaje, facilita la comparación de la dispersión relativa entre diferentes canales de ECG. Estos cálculos validan la coherencia de los resultados obtenidos mediante herramientas estadísticas automatizadas.
Media: Se recorre la señal, sumando todos los valores y dividiendo por el número total de muestras.                                       
```
def calcular_media(datos):
    sumita=0
    for i in datos:
       sumita+= i
    return sumita/ len(datos)
```
Desviación Estándar: Se calcula la dispersión de los datos respecto a la media, obteniendo la varianza y extrayendo su raíz cuadrada.                                                          
                  ![image](https://github.com/user-attachments/assets/6aabccd0-6329-4b82-9047-4379703cc730)
```
def calcular_desviacion(datos, media):
    suma_v=0
    for i in datos:
        suma_v+=(i-media)**2
    varianza=suma_v/len(datos)
    return varianza ** 0.5
```
Coeficiente de Variación:  Se obtiene dividiendo la desviación estándar entre la media y expresando el resultado en porcentaje.                                                                                                     
               ![image](https://github.com/user-attachments/assets/d2f307d1-c7e0-401b-acdd-bb55fd6a1b8a)
```
def calcular_coef_variacion(media, desviacion):
    return (desviacion / media) * 100
```
Este fragmento de código recorre cada canal de la señal ECG. senal.T es la transposición de la matriz senal, que tiene un tamaño de (n_muestras, n_canales), donde cada columna representa un canal ECG. Al hacer .T (transpuesta), obtenemos una estructura de (n_canales, n_muestras), lo que facilita iterar sobre cada canal. enumerate(senal.T) nos proporciona tanto el índice i como el canal, que es una lista de valores de amplitud para ese canal específico. Después se llaman las funciones previamente definas para realizar los cálculos correspondientes en cada iteración sobre la señal.
```
for i, canal in enumerate(senal.T):  # Iterar por canal
    media_manual = calcular_media(canal)
    desviacion_manual = calcular_desviacion(canal, media_manual)
    coef_variacion_manual = calcular_coef_variacion(media_manual, desviacion_manual)
```
>[!WARNING]
>Si no iteras la señal, el código no podrá calcular estadísticas correctamente dado que la señal tiene múltiples canales.

![image](https://github.com/user-attachments/assets/e4acbcaa-d748-469e-a2ca-aabfbfcc66d2)

Histograma:
La línea primera establece el tamaño de la figura del gráfico a 10 pulgadas de ancho por 6 pulgadas de alto. 
```
plt.figure(figsize=(10, 6))
```
A continuación, se genera un histograma de 60 barras con la señal ECG de 10 segundos, con barras azules, bordes negros y opacidad del 70%, además de superponer una curva KDE para mostrar la distribución continua de las amplitudes.
```
sns.histplot(senal_10s, bins=60, color='blue', edgecolor='black', alpha=0.7, kde=True)
```
![image](https://github.com/user-attachments/assets/ad9f24f1-fbf0-4e82-a83a-54ee11552f9a)
## Estadísticos descriptivos (Funciones)
El código calcula tres estadísticas clave de la señal ECG por canal usando la libreria Numpy. La media se obtiene para cada canal, proporcionando el valor promedio de la señal. La desviación estándar mide la dispersión de los datos respecto a la media, utilizando un denominador de n-1 para asegurar una estimación insesgada. Finalmente, el coeficiente de variación se calcula como el cociente entre la desviación estándar y la media, expresado como un porcentaje. Este coeficiente proporciona una medida de la variabilidad relativa de la señal en relación con su media, permitiendo comparar la dispersión entre señales de diferentes magnitudes.
```
# Calcular estadísticas usando numpy
media = np.mean(senal, axis=0)  # Media por canal
desviacion = np.std(senal, axis=0, ddof=1)  # Desviación estándar por canal
coef_variacion = (desviacion / media) * 100  # Coeficiente de variación (%)
```
![image](https://github.com/user-attachments/assets/7c0142ec-d63f-4acd-8ffc-bdc5edcd8128)

# SNR para los distintos tipos de ruidos
El SNR (Signal to noise ratio) o sea relación señal ruido es un parámetro que se utiliza para saber que tan contaminada está una señal, esto se hace comparando la amplitud de la señal, con la amplitud del ruido usando la siguiente fórmula: $SNR = 10 \log_{10} \left(\frac{P_{\text{señal}}}{P_{\text{ruido}}}\right)$

Obtener SNR alto significa que la señal es significativamente más alta que el ruido, esto es importante sobre todo en aplicaciones biomédicas, ya que un SNR alto nos proporciona mayor precisión en los diagnósticos y más facilidad para procesar una señal, un SNR se considera alto a partir de 10 dB lo que se interpreta como que la señal es 10 veces más fuerte que el ruido.

![image](https://github.com/user-attachments/assets/9217c48a-133a-43e2-84c1-d3a99e94dc4a)

Para las señales contaminadas con ruido gaussiano se obtuvieron SNR de 7,89 dB y 31,01 dB, el SNR de 7,89 dB  significa que la señal tiene 6,2 veces la potencia del ruido, por lo que no es aceptable, en cuanto a la otra señal su potencia es 1262 veces mayor a la del ruido, es decir es de muy buena calidad. En amarillo se ve la señal con SNR de 7,89 dB y en rojo la señal con SNR de 31,01 dB
![image](https://github.com/user-attachments/assets/5e0e328d-011e-4381-a4ae-fa93b000a8ba)

Para las señales con ruido de artefacto el primer SNR fue de 0,43 decibeles, esto quiere decir que la señal y el ruido tienen casi la misma potencia, por lo que esa señal es prácticamente inservible, en cuanto a la otra con un SNR de 13,91 dB, esta señal tiene 24,6 veces la potencia del ruido con el que está contaminada lo que la hace aceptable. En morado se ve la señal con SNR de 0,43 dB y en verde la señal con SNR de 13,91 dB.
![image](https://github.com/user-attachments/assets/e12101e0-0956-45d9-89ae-910bc08475a7)
![image](https://github.com/user-attachments/assets/38a76738-48a8-4810-b3a9-8f880ee5b329)
En cuanto a las señales contaminadas con ruido tipo impulso, se obtuvo la primera con SNR de 6,86 dB es decir con unas 4,8 veces la potencia de su ruido, y la otra que tuvo el SNR más alto de todos con 34,42 y una potencia de 2766 veces mayor que el ruido. En color rojo se observa la imagen con SNR de 6,86 dB y en azul la señal con SNR de 34,42 dB.
![image](https://github.com/user-attachments/assets/8a15dfd6-30c2-411f-8501-c6a24e6792ef)
## Bibliografía 
Cita publicación original:
T Penzel, GB Moody, RG Mark, AL Goldberger, JH Peter. The Apnea-ECG Database. Computers in Cardiology 2000;27:255-258.
Cita Physionet:
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.
## Colaboradores
* Catalina Martinez 
* Pablo Acevedo
* Laura Avila
