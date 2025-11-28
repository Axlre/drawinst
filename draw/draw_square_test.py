import pyautogui
import time

# --- Configuración ---
OFFSET_X = 400  # Coordenada X inicial
OFFSET_Y = 300  # Coordenada Y inicial
SQUARE_SIZE = 150 # Tamaño del lado del cuadrado en píxeles
DRAW_DURATION = 0.05 # Velocidad de dibujo (más bajo = más rápido)

START_DELAY = 5 # Segundos de espera antes de empezar a dibujar
# --- Fin de la Configuración ---

def draw_square(start_x, start_y, size, duration):
    """
    Dibuja un cuadrado simple usando PyAutoGUI.
    """
    print(f"Dibujando un cuadrado en ({start_x}, {start_y}) de tamaño {size}...")
    pyautogui.PAUSE = 1 # Pequeña pausa entre acciones

    # Mover al punto de inicio
    pyautogui.moveTo(start_x, start_y, duration=0.1)

    # Bajar el clic
    pyautogui.mouseDown()

    # Dibujar el cuadrado
    pyautogui.dragTo(start_x + size, start_y, duration=duration)       # Derecha
    pyautogui.dragTo(start_x + size, start_y + size, duration=duration) # Abajo
    pyautogui.dragTo(start_x, start_y + size, duration=duration)       # Izquierda
    pyautogui.dragTo(start_x, start_y, duration=duration)             # Arriba (cerrar)

    # Soltar el clic
    pyautogui.mouseUp()
    print("Cuadrado dibujado.")

def main():
    pyautogui.FAILSAFE = True

    print("El script dibujará un cuadrado en:")
    for i in range(START_DELAY, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("¡Dibujando!")

    draw_square(OFFSET_X, OFFSET_Y, SQUARE_SIZE, DRAW_DURATION)
    print("Prueba de dibujo de cuadrado completada.")

if __name__ == "__main__":
    main()