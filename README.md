# Analisis estadistico de un ECG
# Descripción
Señal ECG
La señal utilizada fue extraída de Physionet de la base de datos Apnea-ECG Database, esta base de datos consiste en 70 grabaciones de larga duración (entre 7 y 10 horas) para investigar la apnea del sueño a través de señales de ECG. Cada grabación incluye una señal de ECG de 100 muestras por segundo. 
Se utilizó en a04.hea y el a04.dat, el .hea es un archivo de texto que describe el contenido de .dat, este tiene información como el número de señales, la frecuencia de muestreo, el formato de los datos y la escala de conversión de los valores digitales a unidades fisiológicas.

Link de Apnea-ECG Database: https://physionet.org/content/apnea-ecg/1.0.0/
Estos archivos se cargan en una IDE para Python y se utilizó la librería wfdb (Waveform Database), la cual es utilizada para visualizar señales fisiológicas, como los ECG.
![image](https://github.com/user-attachments/assets/f04279a9-ab89-42ee-86ec-ad7169d4fb11)

Finalmente se trabajó con los primeros diez segundos para poder visualizar mejor la señal con los diferentes ruidos, así como reducir el uso de memoria y almacenamiento ya que la señal original tiene una duración de más de 7 horas.
![image](https://github.com/user-attachments/assets/dbae2ed2-b637-4fea-9660-6694fbf5a2ad)

La señal obtenida representa es un registro de la actividad eléctrica del corazón a lo largo 10 segundos, siendo esta la de una persona con apnea del sueño, con una frecuencia de muestreo de  100Hz

 ![image](https://github.com/user-attachments/assets/900c061d-6d4a-4315-84b3-0efc6ffd7480)
 
                               
Cita publicación original:
T Penzel, GB Moody, RG Mark, AL Goldberger, JH Peter. The Apnea-ECG Database. Computers in Cardiology 2000;27:255-258.

Cita Physionet:
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.
# SNR para los distintos tipos de ruidos
El SNR (Signal to noise ratio) o sea relación señal ruido es un parámetro que se utiliza para saber que tan contaminada está una señal, esto se hace comparando la amplitud de la señal, con la amplitud del ruido usando la siguiente fórmula: $SNR = 10 \log_{10} \left(\frac{P_{\text{señal}}}{P_{\text{ruido}}}\right)$


Obtener SNR alto significa que la señal es significativamente más alta que el ruido, esto es importante sobre todo en aplicaciones biomédicas, ya que un SNR alto nos proporciona mayor precisión en los diagnósticos y más facilidad para procesar una señal, un SNR se considera alto a partir de 10 dB lo que se interpreta como que la señal es 10 veces más fuerte que el ruido.


![image](https://github.com/user-attachments/assets/9217c48a-133a-43e2-84c1-d3a99e94dc4a)

Para las señales contaminadas con ruido gaussiano se obtuvieron SNR de 7,89 dB y 31,01 dB, el SNR de 7,89 dB  significa que la señal tiene 6,2 veces la potencia del ruido, por lo que no es aceptable, en cuanto a la otra señal su potencia es 1262 veces mayor a la del ruido, es decir es de muy buena calidad. En amarillo se ve la señal con SNR de 7,89 dB y en rojo la señal con SNR de 31,01 dB
![image](https://github.com/user-attachments/assets/5e0e328d-011e-4381-a4ae-fa93b000a8ba)


Para las señales con ruido de artefacto el primer SNR fue de 0,43 decibeles, esto quiere decir que la señal y el ruido tienen casi la misma potencia, por lo que esa señal es prácticamente inservible, en cuanto a la otra con un SNR de 13,91 dB, esta señal tiene 24,6 veces la potencia del ruido con el que está contaminada lo que la hace aceptable.

En cuanto a las señales contaminadas con ruido tipo impulso, se obtuvo la primera con SNR de 6,86 dB es decir con unas 4,8 veces la potencia de su ruido, y la otra que tuvo el SNR más alto de todos con 34,42 y una potencia de 2766 veces mayor que el ruido


                         
