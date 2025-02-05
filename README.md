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

                         
