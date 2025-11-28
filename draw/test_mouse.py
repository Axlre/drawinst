import pyautogui
import time

# Pon el Failsafe por si acaso
pyautogui.FAILSAFE = True

print("Iniciando prueba de mouse en 3 segundos...")
print("NO HAGAS CLIC EN NINGUNA VENTANA.")
print("Solo suelta el mouse y mira si se mueve solo.")
time.sleep(3)

print("Moviendo el mouse al centro (500, 500)...")
pyautogui.moveTo(500, 500, duration=1)
print("Mouse movido. ¿Lo viste?")
time.sleep(1)

print("Moviendo el mouse a (800, 500)...")
pyautogui.moveTo(800, 500, duration=1)
print("Prueba terminada.")