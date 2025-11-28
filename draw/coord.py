# Este es un script separado para encontrar tus coordenadas
import pyautogui
import time

print("--- CÓMO USAR ESTO ---")
print("1. Abre tu programa de dibujo (Paint, etc.)")
print("2. Mueve este terminal a un lado para que puedas ver el área de dibujo.")
print("3. Tienes 5 segundos para mover el mouse a la esquina SUPERIOR IZQUIERDA donde quieres que el dibujo COMIENCE.")
print("-------------------------")

for i in range(5, 0, -1):
    print(f"Mueve tu mouse... {i}")
    time.sleep(1)

# Captura la posición actual del mouse
pos = pyautogui.position()

print("\n--- ¡LISTO! ---")
print(f"Tu posición es: {pos}")
print("\nCopia y pega las siguientes dos líneas en tu script 'draw_svg.py':")
print("-------------------------")
print(f"OFFSET_X = {pos.x}")
print(f"OFFSET_Y = {pos.y}")
print("-------------------------")