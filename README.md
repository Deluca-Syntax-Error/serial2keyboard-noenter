# Control Remoto para PC con Arduino y Python

## Proyecto técnico – Escuela Técnica N°2 de Munro  
**Autores:** Fabricio Deluca, Ezequiel Giménez y Thiago Robledo  

---

## Descripción del Proyecto  

Este proyecto tiene como objetivo controlar un sistema Windows mediante un control remoto infrarrojo reciclado, utilizando un **Arduino Uno** y un **lector IR** reutilizado.  

El sistema permite ejecutar acciones comunes sin necesidad de teclado ni ratón, ofreciendo una forma alternativa de interacción con la computadora.  

El **Arduino** recibe señales del control remoto, las interpreta y las envía por **puerto USB** a un script de **Python**, el cual ejecuta las acciones correspondientes en el sistema operativo.  

Además, el programa informa por voz cada acción realizada utilizando la librería `pyttsx3`, simulando el comportamiento de un asistente virtual.  

---

## Funcionalidades Principales  

- Abrir **Google** directamente desde el control remoto.  
- Acceder rápidamente a **redes sociales** como Facebook, Instagram o YouTube.  
- Abrir **Gmail** en el navegador predeterminado.  
- Lanzar el **Explorador de archivos**.  
- Mostrar un **teclado en pantalla** libre de uso:  
  [Free Virtual Keyboard](https://freevirtualkeyboard.com/virtualkeyboard/)  
- Confirmación por voz mediante `pyttsx3`, informando la acción realizada.  

---

## Componentes Utilizados  

### Hardware  
- **Arduino UNO**  
- **Sensor IR** (receptor infrarrojo reciclado)  
- **Control remoto infrarrojo antiguo**  
- **Cable USB** para conexión con PC  

### Software  
- **Python 3** (en sistema Windows)  
- Librerías Python:
  - `pyserial` (comunicación con Arduino)
  - `os` y `subprocess` (ejecución de programas)
  - `pyttsx3` (síntesis de voz)
- **Arduino IDE**  
- **Free Virtual Keyboard** (uso libre, no requiere instalación)  

---

## Funcionamiento General  

1. El **Arduino UNO** capta las señales IR del control remoto.  
2. Traduce cada señal en un **código único** y lo envía por el puerto **serial USB** al sistema.  
3. El script en **Python** recibe los datos, los interpreta y ejecuta la acción correspondiente en Windows.  
4. El sistema **anuncia por voz** la acción ejecutada gracias a `pyttsx3`.  

---

## Ejemplo de Uso  

| Botón del control | Acción en Windows              | Voz del sistema                  |
|-------------------|--------------------------------|----------------------------------|
| 2                 | Abre Google Chrome             | "Abriendo Google"                |
| 6                 | Abre Gmail                     | "Abriendo Gmail"                 |
| 1                 | Abre el teclado virtual         | "Mostrando teclado en pantalla"  |
| 7                 | Abre el explorador de archivos | "Abriendo explorador"            |

---

## Asistente por Voz  

El sistema utiliza **pyttsx3**, una librería libre que permite la **síntesis de voz sin conexión a internet**.  
Esto brinda una experiencia similar a la de un **asistente virtual**, totalmente local y personalizable.  

---

## Objetivo Educativo  

Este proyecto fue desarrollado como parte de una práctica técnica en la **Escuela Técnica N°2 de Munro**, con el objetivo de:  

- Aplicar conocimientos de **electrónica y programación**.  
- Reutilizar **componentes electrónicos** (control remoto y sensor IR).  
- Integrar **Arduino con Python** para crear una interfaz hombre-máquina accesible.  
- Promover soluciones de **accesibilidad y control remoto**.  

---

## Instalación y Uso  

### 1. Arduino  
Cargar el código `.ino` en el Arduino UNO usando el **Arduino IDE**.  
Conectar el sensor IR al pin definido en el código (por defecto, pin 11).  

### 2. Python  
Instalar dependencias:  
```bash
pip3 install pyserial pyttsx3
```
Ejecutar script
```bash
python3 --port PORT --BAUD BAUD
```
### 3. Control remoto
Apuntar al sensor IR y presionar un botón para ejecutar la acción asignada.

## Licencias y Créditos
- Free Virtual Keyboard – Software libre de uso: https://freevirtualkeyboard.com/virtualkeyboard/
- Código del proyecto bajo licencia GPLv3.
- Desarrollado por Fabricio Deluca, Ezequiel Giménez y Thiago Robledo, con fines educativos para la Técnica 2 de Munro.

## Contacto
Técnica 2 de Munro – 7'2 Proyecto IRIS (2025)
