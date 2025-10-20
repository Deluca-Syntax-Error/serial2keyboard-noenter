import os
import time
import webbrowser
import re
import argparse
import threading
import queue

import serial  
import pyttsx3
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

# --- Inicializaciones globales (objetos) ---
mouse = MouseController()
keyboard = KeyboardController()

# Variable que controla si mover el mouse o enviar flechas
movermouse = True

# Código serial -> número de acción (1..21)
SERIAL_CODE_TO_ACTION = {
    11789: 1,
    3058: 2,
    2034: 3,
    18930: 4,
    2545: 5,
    19443: 6,
    14348: 7,
    16907: 8,
    17419: 9,
    17932: 10,
    18443: 11,
    18956: 12,
    19468: 13,
    19981: 14,
    20491: 15,
    21004: 16,
    16394: 17,
    12812: 18,
    1229: 19,
    15373: 20,
    15886: 21
}

# --- TTS (pyttsx3) en segundo plano con cola ---
_tts_queue = queue.Queue()
_tts_thread = None

def _tts_worker(q: queue.Queue):
    engine = pyttsx3.init()
    # Opcionales: ajustar velocidad y volumen
    try:
        rate = engine.getProperty('rate')
        engine.setProperty('rate', max(120, rate - 20))
    except Exception:
        pass
    try:
        vol = engine.getProperty('volume')
        engine.setProperty('volume', vol)
    except Exception:
        pass

    while True:
        text = q.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            # no queremos que falle el worker completo
            pass
    try:
        engine.stop()
    except Exception:
        pass

def start_tts_thread():
    global _tts_thread
    if _tts_thread is None:
        _tts_thread = threading.Thread(target=_tts_worker, args=(_tts_queue,), daemon=True)
        _tts_thread.start()

def stop_tts_thread():
    # enviar sentinel None y esperar un poco
    try:
        _tts_queue.put_nowait(None)
    except Exception:
        pass
    if _tts_thread is not None:
        _tts_thread.join(timeout=1.0)

def speak_async(text: str):
    # encolar texto; si por alguna razón la cola está llena, lo ignoramos
    try:
        _tts_queue.put_nowait(text)
    except queue.Full:
        pass

# Helper: limpia la línea para extraer un entero
def extract_int_from_line(line: str):
    m = re.search(r"-?\d+", line)
    if m:
        try:
            return int(m.group())
        except ValueError:
            return None
    return None

# Acción principal (match-case; requiere Python >=3.10)
def ejecutar_accion(opcion):
    global movermouse

    # Opciones 3-6 (movimiento) NO harán TTS según tu pedido.
    match opcion:
        case 1:
            print("Apagando sistema...")
            speak_async("Apagando el equipo")
            os.system("shutdown /s /t 1")

        case 2:
            if movermouse:
                print("Clic izquierdo")
                mouse.click(Button.left)
                speak_async("Click realizado")
            else:
                print("Presionar Enter")
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                speak_async("Enter presionado")

        case 3:
            if movermouse:
                x, y = mouse.position
                mouse.position = (x, y - 50)
                print("Mover mouse arriba")
            else:
                print("Presionar flecha arriba")
                keyboard.press(Key.up)
                keyboard.release(Key.up)

        case 4:
            if movermouse:
                x, y = mouse.position
                mouse.position = (x - 50, y)
                print("Mover mouse izquierda")
            else:
                print("Presionar flecha izquierda")
                keyboard.press(Key.left)
                keyboard.release(Key.left)

        case 5:
            if movermouse:
                x, y = mouse.position
                mouse.position = (x, y + 50)
                print("Mover mouse abajo")
            else:
                print("Presionar flecha abajo")
                keyboard.press(Key.down)
                keyboard.release(Key.down)

        case 6:
            if movermouse:
                x, y = mouse.position
                mouse.position = (x + 50, y)
                print("Mover mouse derecha")
            else:
                print("Presionar flecha derecha")
                keyboard.press(Key.right)
                keyboard.release(Key.right)

        case 7:
            movermouse = not movermouse
            estado = "activado" if movermouse else "desactivado"
            print(f"movermouse ahora es {movermouse}")
            speak_async(f"Modo ratón {estado}")

        case 8:
            print("Abrir programa 'vk' (start vk)")
            speak_async("Abriendo el programa de teclado")
            os.system("start vk")

        case 9:
            print("Abrir Google")
            speak_async("Abriendo Google")
            webbrowser.open("https://www.google.com")

        case 10:
            print("Abrir YouTube")
            speak_async("Abriendo YouTube")
            webbrowser.open("https://www.youtube.com")

        case 11:
            print("Abrir Facebook")
            speak_async("Abriendo Facebook")
            webbrowser.open("https://www.facebook.com")

        case 12:
            print("Abrir Instagram")
            speak_async("Abriendo Instagram")
            webbrowser.open("https://www.instagram.com")

        case 13:
            print("Abrir Gmail")
            speak_async("Abriendo Gmail")
            webbrowser.open("https://mail.google.com")

        case 14:
            print("Abrir Explorador de archivos")
            speak_async("Abriendo el explorador de archivos")
            os.system("start explorer")

        case 15:
            path_img = "tutorial.png"
            print(f"Abrir imagen: {path_img}")
            try:
                os.startfile(path_img)
                speak_async("Abriendo imagen de tutorial")
            except OSError as e:
                print(f"No se pudo abrir la imagen: {e}")
                speak_async("No se pudo abrir la imagen")

        case 16:
            print("Aumentar zoom (Ctrl + '+')")
            with keyboard.pressed(Key.ctrl):
                keyboard.press('+')
                keyboard.release('+')
            speak_async("Aumentando zoom")

        case 17:
            print("Reducir zoom (Ctrl + '-')")
            with keyboard.pressed(Key.ctrl):
                keyboard.press('-')
                keyboard.release('-')
            speak_async("Reduciendo zoom")

        case 18:
            print("Minimizar (Win + Down)")
            with keyboard.pressed(Key.cmd):
                keyboard.press(Key.down)
                keyboard.release(Key.down)
            speak_async("Ventana minimizada")

        case 19:
            print("Maximizar (Win + Up)")
            with keyboard.pressed(Key.cmd):
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            speak_async("Ventana maximizada")

        case 20:
            print("Subir volumen (teclas multimedia)")
            speak_async("Subiendo volumen")
            try:
                for _ in range(3):
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
                    time.sleep(0.05)
            except AttributeError:
                print("Key.media_volume_up no disponible, intentando nircmd...")
                os.system("nircmd.exe changesysvolume 5000")

        case 21:
            print("Bajar volumen (teclas multimedia)")
            speak_async("Bajando volumen")
            try:
                for _ in range(3):
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)
                    time.sleep(0.05)
            except AttributeError:
                print("Key.media_volume_down no disponible, intentando nircmd...")
                os.system("nircmd.exe changesysvolume -5000")

        case _:
            print("Opción no válida:", opcion)
            speak_async("Opción no válida")

def main(port: str, baud: int, timeout: float, debounce_seconds: float):
    last_seen = {}  # codigo -> timestamp
    start_tts_thread()

    try:
        ser = serial.Serial(port, baud, timeout=timeout)
        print(f"Abierto puerto serial {port} a {baud}bps (timeout={timeout}s)")
    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto serial {port}: {e}")
        stop_tts_thread()
        return

    try:
        while True:
            try:
                raw = ser.readline()
                if not raw:
                    continue

                try:
                    line = raw.decode(errors="ignore").strip()
                except Exception:
                    line = str(raw).strip()

                codigo = extract_int_from_line(line)
                if codigo is None:
                    continue

                ahora = time.time()
                last = last_seen.get(codigo, 0)
                if ahora - last < debounce_seconds:
                    continue
                last_seen[codigo] = ahora

                accion = SERIAL_CODE_TO_ACTION.get(codigo)
                if accion is None:
                    print(f"Código desconocido recibido: {codigo} (line: '{line}')")
                    speak_async("Código desconocido")
                    continue

                print(f"Recibido código {codigo} -> acción {accion}")
                ejecutar_accion(accion)

            except KeyboardInterrupt:
                print("Interrumpido por usuario. Saliendo...")
                break
            except Exception as e:
                print("Error leyendo serial o ejecutando acción:", e)
                # seguir intentando
                time.sleep(0.1)

    finally:
        try:
            ser.close()
        except Exception:
            pass
        stop_tts_thread()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Controlador por serial que ejecuta acciones en Windows según códigos recibidos (con TTS).")
    parser.add_argument("--port", "-p", type=str, required=True,
                        help="Puerto serial (ej: COM3)")
    parser.add_argument("--baud", "-b", type=int, default=9600,
                        help="Baudrate (por defecto: 9600)")
    parser.add_argument("--timeout", "-t", type=float, default=1.0,
                        help="Timeout de lectura en segundos (por defecto: 1.0)")
    parser.add_argument("--debounce", "-d", type=float, default=0.5,
                        help="Segundos para ignorar lecturas repetidas del mismo código (por defecto: 0.5)")

    args = parser.parse_args()
    main(args.port, args.baud, args.timeout, args.debounce)

