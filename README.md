# Preparación-laboratorio-Nav2
Repositorio preparación práctica laboratorio con Nav2

**TurtleBot3 + LiDAR** en **ROS 2 Jazzy** y **Gazebo**. Sobre un escanario y pauqete nuevos creados, se construye un mapa mediante **mapeo teleoperado (SLAM)** y luego se reutiliza ese mapa para la **navegación autónoma** con localización **AMCL** y la planificación/control de **Nav2**.
## Video funcionamiento
https://youtu.be/GaFDvxMamDc

## Descripción

El flujo se divide en dos etapas con una diferencia clara:

- **Mapeo (SLAM):** el robot se conduce **manualmente con el teclado** para recorrer el escenario y construir el mapa. El operador dirige el robot.
<img width="300" src="https://github.com/user-attachments/assets/8020aa04-f0fb-4a31-8249-b4cfdbe717c3" />

- **Navegación autónoma (AMCL):** el mapa guardado se usa como entorno fijo. El robot **se localiza solo** dentro del mapa y navega de forma autónoma a los objetivos, sin intervención manual.
<img width="300" src="https://github.com/user-attachments/assets/30922fa8-aa96-4707-b722-339d2b8fe442" />


## Requisitos

- Proyecto base de la primera parte (`mi_paquete_nav` + escenario + mapa).
- Paquete de teleoperación por teclado:

```bash
sudo apt install ros-jazzy-teleop-twist-keyboard
```

## Etapa 1 — Mapeo teleoperado

**Terminal 1** — simulación en modo SLAM:

```bash
cd ~/ros2_ws && source install/setup.bash
ros2 launch mi_paquete_nav escenario_nav.launch.py
```

**Terminal 2** — teleoperación por teclado:

```bash
cd ~/ros2_ws && source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

> La ventana del teleop debe tener el **foco** (clic encima) para captar las teclas.
> Teclas: `i` adelante · `,` atrás · `j` girar izq. · `l` girar der. · `k` parar.

Recorrer todo el escenario (perímetro y obstáculos) observando cómo se construye el mapa en RViz.

## Etapa 2 — Guardar el mapa

```bash
ros2 run nav2_map_server map_saver_cli \
  -f ~/ros2_ws/src/mi_paquete_nav/maps/mi_mapa
```

Genera `mi_mapa.pgm` (imagen de ocupación) y `mi_mapa.yaml` (metadatos).

## Etapa 3 — Navegación autónoma

```bash
cd ~/ros2_ws && source install/setup.bash
ros2 launch mi_paquete_nav escenario_localization.launch.py
```

En RViz, con el mapa ya cargado de fondo:

1. **`2D Pose Estimate`** — indicar la posición y orientación inicial del robot sobre el mapa (paso necesario para que AMCL localice).
2. **`Nav2 Goal`** — marcar el destino. El robot planifica la trayectoria y navega de forma autónoma evitando los obstáculos.

## Verificación

```bash
ros2 run tf2_tools view_frames   # En navegación, la relación map -> odom la aporta AMCL
```

En el panel **Navigation 2** de RViz, `Localization` debe aparecer **active**.

## Diferencia clave SLAM vs. Localización

| | Mapeo (SLAM) | Navegación autónoma (AMCL) |
|---|---|---|
| Mapa | Se construye en tiempo real | Fijo, cargado desde disco |
| Movimiento | Manual (teclado) | Autónomo (Nav2) |
| Pose inicial | No requerida | Requerida (`2D Pose Estimate`) |

## Notas

- Un mapa con buena cobertura mejora notablemente la convergencia de AMCL.
- La planificación y el control los proporciona Nav2 con sus planificadores y controladores por defecto.
