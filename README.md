# MSIFanControl-Linux

[English](#english) | [Español](#español)

---

<a name="english"></a>
# English

A simple PySide6 graphical interface for managing MSI laptop fans on Linux distributions.

## Why this project?
This project was born out of the need to control the temperature of my MSI laptop, which tended to overheat under heavy workloads. By using `isw` to interact with the Embedded Controller (EC), I decided to create this GUI to quickly and visually toggle between Turbo mode and Normal mode.

## Requirements
- `isw` (MSI EC tools) installed.
- Root privileges (via `kdesu` or `sudo`).

## Installation
1. Clone the repository: `git clone https://github.com/JuanARamirez97/MSIFanControl-Linux.git`
2. Navigate to the folder: `cd MSIFanControl-Linux`
3. If `isw` is not installed, follow the instructions at [isw GitHub repository](https://github.com/yottatsa/isw).
4. Run the installer: `python3 install.py`
5. Launch "MSI Fan Control" from your application menu. It will prompt for your administrator password automatically.

## Updating the project
If there is a new update available, simply run the following command in the project folder to pull the latest changes and reconfigure your installation:
`python3 update.py`

---

<a name="español"></a>
# Español

Una interfaz gráfica sencilla en PySide6 para gestionar los ventiladores de portátiles MSI en distribuciones Linux.

## ¿Por qué este proyecto?
Este proyecto nació de la necesidad de controlar la temperatura de mi laptop MSI, la cual tendía a calentarse bajo cargas de trabajo intensas. Al usar `isw` para interactuar con el controlador embebido (EC), decidí crear esta GUI para alternar entre el modo Turbo y el modo Normal de forma rápida y visual.

## Requisitos
- Tener instalado `isw` (MSI EC tools).
- Privilegios de root (via `kdesu` o `sudo`).

## Instalación
1. Clona el repositorio: `git clone https://github.com/JuanARamirez97/MSIFanControl-Linux.git`
2. Entra en la carpeta: `cd MSIFanControl-Linux`
3. Si no tienes instalado `isw`, sigue las instrucciones en el [repositorio de isw](https://github.com/yottatsa/isw).
4. Ejecuta el instalador: `python3 install.py`
5. Lanza "MSI Fan Control" desde tu menú de aplicaciones. Te solicitará la contraseña de administrador automáticamente.

## Actualizar el proyecto
Si hay una nueva actualización disponible, simplemente ejecuta el siguiente comando en la carpeta del proyecto para descargar los cambios y actualizar tu instalación:
`python3 update.py`