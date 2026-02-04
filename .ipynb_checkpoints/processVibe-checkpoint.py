from pymavlink import mavutil
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
# Reemplaza con la ruta a tu archivo .BIN descargado del Pixhawk
log_file = 'ruta/a/tu/log_de_vuelo.BIN' 

# Conectar con el log
print(f"Leyendo log: {log_file}...")
mlog = mavutil.mavlink_connection(log_file)

# Listas para almacenar datos
data = {'TimeUS': [], 'VibeX': [], 'VibeY': [], 'VibeZ': [], 'Clip0': []}

# --- EXTRACCIÓN DE DATOS ---
while True:
    msg = mlog.recv_match(type='VIBE', blocking=False)
    if not msg:
        break
    
    # Extraer datos del mensaje VIBE
    data['TimeUS'].append(msg.TimeUS)
    data['VibeX'].append(msg.VibeX)
    data['VibeY'].append(msg.VibeY)
    data['VibeZ'].append(msg.VibeZ)
    data['Clip0'].append(msg.Clip0)

# Crear DataFrame
df = pd.DataFrame(data)
# Convertir tiempo a segundos (TimeUS está en microsegundos desde el arranque)
df['TimeSec'] = (df['TimeUS'] - df['TimeUS'].iloc[0]) / 1e6

# --- GRAFICACIÓN (Estilo APA / Académico) ---
# Norma APA sugiere fuentes sans-serif (Arial, Calibri) dentro de figuras 
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

fig, ax = plt.subplots(figsize=(10, 6))

# Graficar Vibraciones
ax.plot(df['TimeSec'], df['VibeX'], label='Vibe X', linewidth=1)
ax.plot(df['TimeSec'], df['VibeY'], label='Vibe Y', linewidth=1)
ax.plot(df['TimeSec'], df['VibeZ'], label='Vibe Z', linewidth=1)

# Configuración de ejes y etiquetas
ax.set_xlabel('Tiempo (segundos)', fontsize=11, fontweight='bold')
ax.set_ylabel('Vibración (m/s²)', fontsize=11, fontweight='bold')
ax.set_title('Análisis de Vibraciones durante el Vuelo', fontsize=12, style='italic') # Título descriptivo [cite: 1608]
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# Guardar en alta resolución
plt.savefig('grafica_vibraciones_apa.png', dpi=300, bbox_inches='tight')
plt.show()

print("Gráfica generada exitosamente.")