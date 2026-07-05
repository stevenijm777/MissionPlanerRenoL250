# Mission Planner & Integración Mecatrónica - Reno L250 UAV

Este repositorio contiene los archivos de software, diseño mecánico CAD 3D, planos de fabricación, parámetros del piloto automático y scripts de análisis de telemetría utilizados en el proyecto de titulación y artículo de investigación: **"Integración mecatrónica y validación de una plataforma UAV de ala fija de bajo costo basada en arquitectura abierta"** (ESPOL).

El enfoque de este repositorio está orientado a la plataforma comercial **Reno L250** convertida de combustión interna a propulsión eléctrica pura para investigación en vuelo autónomo.

---

## 🔗 Repositorio de Simulación (Gemelo Digital)
Para complementar las pruebas en hardware físico con simulaciones de alta fidelidad, se ha desarrollado un Gemelo Digital en **NVIDIA Isaac Sim** empleando **Pegasus Simulator**. 
* El repositorio con el script de simulación de la planta aerodinámica y el entorno 3D está disponible en: [isaac-uav (GitHub)](https://github.com/stevenijm777/isaac-uav)
* Ruta local para contexto: `C:\Users\steve\Documents\GitRepositories\isaac-uav`

---

## 📂 Estructura del Repositorio

El repositorio se organiza de la siguiente manera:

```text
MissionPlanerRenoL250/
├── 12_Codigos_Graficas/   # Jupyter Notebook y scripts de Python para procesamiento de logs .BIN
├── Calculos/              # Hoja de cálculo verificada de diseño dinámico e importación
├── Manual_RENOL250/       # Escaneos del manual físico de ensamblaje del Reno L250
├── Modelo3D/              # Archivos CAD Autodesk Inventor (.ipt, .iam), STLs impresiones y planos PDF
├── Parametros/            # Archivos de respaldo de parámetros (.param) de ArduPilot
├── Guia_Mission_Planner.pdf # Guía de integración de software y hardware
└── .gitignore             # Configuración de exclusión para logs pesados y temporales CAD
```

### 1. `12_Codigos_Graficas/`
Contiene la algoritmia para análisis post-vuelo de telemetría y vibraciones:
* **`processVibe.py`**: Script en Python para extraer datos del mensaje `VIBE` del log de vuelo `.BIN` y generar gráficas de vibraciones en los ejes X, Y y Z en alta resolución bajo normas APA.
* **`missionPlanning.ipynb`**: Jupyter Notebook interactivo que procesa la telemetría MAVLink para validar la respuesta de actuadores comparando las entradas del piloto (`RCIN`) frente a las salidas físicas de los servomotores (`RCOUT`) en los canales de guiñada, cabeceo, alabeo y acelerador.
* **Gráficas PNG**: Resultados exportados que muestran la supresión de vibraciones y la validación de latencia cero en la cadena de control.

### 2. `Calculos/`
* **`ANALISIS_COMPLETO_UAV.xlsx`**: Hoja de cálculo dinámica y verificada que consolida el análisis de pesos (MTOW) y estimación aerodinámica de los modelos Foam Board (Manual/Auto), Reno L250 y la variante de alta velocidad (2200KV). Permite calcular de manera automática:
  * Velocidad de pérdida ($V_{stall}$) y carga alar ($WL$) basándose en el coeficiente de sustentación $C_{L_{max}}$ y área alar de diseño.
  * Relación Empuje/Peso ($T/W$) y potencia requerida.
  * Autonomía teórica y práctica (70% de reserva).
  * Desglose completo de importación (FOB EE.UU. a Ecuador sumando aranceles, Fodinfa, fletes por peso y tasas de aduana).

### 3. `Manual_RENOL250/`
* Recopilación de imágenes escaneadas de las instrucciones físicas originales del fuselaje comercial Reno L250. Esencial para conocer la distribución espacial del ala, estabilizadores, y las distancias de montaje recomendadas de fábrica.

### 4. `Modelo3D/`
* **`RenoL250/`**: Modelado 3D en Autodesk Inventor de la aeronave desglosado en ensambles (`.iam`) y partes (`.ipt`) de las alas, fuselaje principal (body), rudder, estabilizador vertical y tren de aterrizaje.
* **`Soporte_Pixhawck/`** y **`MOTOR/`**: Planos CAD de los soportes amortiguados impresos en 3D para el controlador Pixhawk 2.4.8 y el acople de conversión al motor eléctrico KingVal 3548.
* **`STL_Impresion/`**: Archivos `.stl` listos para laminación e impresión en 3D (PLA/PETG) de los soportes de servos, soportes del motor, llantas y trompa protectora.
* **`Planos_PDF_estructura/`**: Planos bidimensionales detallados con acotaciones mecánicas para la fabricación física y de taller.

### 5. `Parametros/`
* Archivos `.param` exportados desde Mission Planner. Incluyen la sintonización de lazos de control PID, límites operacionales de alabeo y cabeceo, configuración de canales PWM y calibración de sensores inerciales del UAV para ArduPilot.

---

##  Requisitos e Instalación

Para ejecutar los scripts de procesamiento de telemetría, se requiere Python 3.8+ y las siguientes dependencias:

```bash
pip install pymavlink pandas matplotlib openpyxl
```

### Ejecutar el análisis de vibraciones:
1. Copia tu archivo de log `.BIN` descargado de la tarjeta MicroSD de la Pixhawk en la carpeta de tu script.
2. Modifica la variable `log_file` en `processVibe.py` apuntando a tu archivo de log (ej. `log_file = '00000009.BIN'`).
3. Ejecuta el script:
   ```bash
   python 12_Codigos_Graficas/processVibe.py
   ```
4. Se generará una gráfica llamada `grafica_vibraciones_apa.png` mostrando la respuesta dinámica de aceleración inercial en $m/s^2$ (umbral seguro Pixhawk: $<30\text{ m/s}^2$).

---

##  Componentes de la Plataforma Reno L250 (Auto)
* **Controlador de Vuelo**: Pixhawk 2.4.8 (Firmware ArduPlane)
* **Módulo GNSS**: NEO-M8N GPS con brújula magnetómetro externa
* **Motor Brushless**: KingVal 3548 1100KV (Conversión eléctrica)
* **ESC (Speed Controller)**: Flycolor 60A ESC (3-6S Lipo)
* **Hélice**: 12x6 pulgadas de madera/nylon
* **Servomotores**: MG996R con engranajes metálicos de torque alto (3 unidades)
* **Batería**: LiPo 3S 2200 mAh (11.1 V)
* **Radiocontrol**: Transmisor Flysky FS-i6X y receptor FS-iA10B (2.4 GHz, 10 Canales)
* **Módulo de Poder (PMU)**: Sensor de corriente y regulador de voltaje 5.3V BEC
