import pyautogui
import time
from xml.dom import minidom
from svg.path import parse_path, Line, Move, CubicBezier, QuadraticBezier
import keyboard  


SVG_FILE = 'reze.svg'   
OFFSET_X = 150 
OFFSET_Y = 850          
IMG_SCALE = 0.070     

DRAW_DURATION = 0.0001
CURVE_STEPS = 5
ROTATE_90_DEGREES = False

START_DELAY = 5         
EMERGENCY_STOP_KEY = 'a' 



def check_for_exit():
    if keyboard.is_pressed(EMERGENCY_STOP_KEY):
        pyautogui.mouseUp()  
        print(f"\n¡DETENCIÓN DE EMERGENCIA SOLICITADA ({EMERGENCY_STOP_KEY})!")
        raise KeyboardInterrupt


def get_paths_from_svg(svg_file):
    print(f"Cargando archivo SVG: {svg_file}")
    try:
        doc = minidom.parse(svg_file)
        path_strings = [path.getAttribute(
            'd') for path in doc.getElementsByTagName('path')]
        doc.unlink()

        all_paths = []
        for d in path_strings:
            all_paths.append(parse_path(d))

        print(
            f"SVG procesado. Se encontraron {len(all_paths)} trazados (sin filtrar).")

        if len(all_paths) == 0:
            print("Error: El SVG no contiene 'paths'.")
            return None
        return all_paths

    except Exception as e:
        print(f"Error fatal leyendo el SVG: {e}")
        return None


def draw_vector_paths(paths, offset_x, offset_y, scale, duration, curve_steps):
    if ROTATE_90_DEGREES:
        pyautogui.PAUSE = 0.0001

    try:
        for path in paths:
            check_for_exit()  

            for segment in path:
                orig_start_x = segment.start.real
                orig_start_y = segment.start.imag
                orig_end_x = segment.end.real
                orig_end_y = segment.end.imag

                if ROTATE_90_DEGREES:
                    start_x = (orig_start_y * scale) + offset_x
                    start_y = (orig_start_x * scale) + offset_y

                    end_x = (orig_end_y * scale) + offset_x
                    end_y = (orig_end_x * scale) + offset_y

                else:
                    start_x = (orig_start_x * scale) + offset_x
                    start_y = (orig_start_y * scale * -1) + offset_y

                    end_x = (orig_end_x * scale) + offset_x
                    end_y = (orig_end_y * scale * -1) + offset_y
                # --- FIN DE LÓGICA DE ROTACIÓN ---

                if isinstance(segment, Move):
                    pyautogui.mouseUp()
                    # El 'moveTo' es rápido, no necesita 'tween'
                    pyautogui.moveTo(end_x, end_y, duration=0.05)

                elif isinstance(segment, Line):
                    pyautogui.mouseDown()
                    pyautogui.dragTo(end_x, end_y, duration=duration *
                                     segment.length(), tween=pyautogui.linear)

                elif isinstance(segment, (CubicBezier, QuadraticBezier)):
                    pyautogui.mouseDown()
                    for i in range(1, curve_steps + 1):
                        check_for_exit()  # Revisar en cada paso de la curva

                        t = i / curve_steps
                        point = segment.point(t)

                        orig_px = point.real
                        orig_py = point.imag

                        # --- LÓGICA DE ROTACIÓN (CURVAS) ---
                        if ROTATE_90_DEGREES:
                            px = (orig_py * scale) + offset_x
                            py = (orig_px * scale) + offset_y
                        else:
                            px = (orig_px * scale) + offset_x
                            py = (orig_py * scale * -1) + offset_y
                        # --- FIN LÓGICA DE ROTACIÓN (CURVAS) ---

                        seg_duration = (
                            duration * segment.length()) / curve_steps
                        pyautogui.dragTo(
                            px, py, duration=seg_duration, tween=pyautogui.linear)

            pyautogui.mouseUp()  # Asegurarse de soltar al final de cada path

    except KeyboardInterrupt:
        # Esto captura la interrupción de nuestra función check_for_exit()
        print("Dibujo detenido por el usuario.")
        pyautogui.mouseUp()  # Por si acaso
        return  # Salimos de la función de dibujo

    print("¡Dibujo completado!")


def main():
    # ¡IMPORTANTE! Activa la parada de emergencia moviendo el mouse
    # a la esquina superior izquierda (0,0).
    pyautogui.FAILSAFE = True

    paths = get_paths_from_svg(SVG_FILE)
    if paths is None:
        return

    # 1. Confirmación de inicio
    try:
        proceed = input("¿Deseas comenzar a dibujar? (s/n): ").strip().lower()
        if proceed != 's':
            print("Dibujo cancelado por el usuario.")
            return
    except KeyboardInterrupt:
        print("\nOperación cancelada.")
        return

    # 2. Cuenta regresiva
    print("El script comenzará a dibujar en:")
    try:
        for i in range(START_DELAY, 0, -1):
            print(f"{i}...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCuenta regresiva cancelada.")
        return

    print("¡Dibujando!")
    print(f"--- ¡PRESIONA '{EMERGENCY_STOP_KEY}' PARA DETENER DE EMERGENCIA! ---")
    print("--- (O mueve el mouse a la esquina superior izquierda) ---")

    # 3. Proceso de dibujo (con manejo de errores)
    try:
        draw_vector_paths(paths, OFFSET_X, OFFSET_Y,
                          IMG_SCALE, DRAW_DURATION, CURVE_STEPS)

    except pyautogui.FailSafeException:
        # Captura la parada de emergencia del mouse en la esquina
        print("\n¡DETENCIÓN DE EMERGENCIA (FAILSAFE) ACTIVADA!")
        pyautogui.mouseUp()

    except KeyboardInterrupt:
        # Captura un Ctrl+C en la terminal (menos probable, pero por si acaso)
        print("\nScript detenido por el usuario.")

    # 4. Pausa final
    print("\n--------------------------------------------------")
    print("   ¡DIBUJO TERMINADO EN PANTALLA!")
    print("   ¡AHORA TOMA EL MOUSE Y PRESIONA 'Enviar' EN INSTAGRAM!")
    print("--------------------------------------------------")

    try:
        input("\n...presiona Enter en esta terminal CUANDO HAYAS TERMINADO...")
    except KeyboardInterrupt:
        print("\nScript finalizado.")

    print("Script finalizado.")


if __name__ == "__main__":
    main()