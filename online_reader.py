import pyautogui
import time

# Задержка перед выполнением, чтобы успеть подготовиться
time.sleep(3)

# Получить текущую позицию мыши (для ориентирования)
current_position = pyautogui.position()
print(f"Текущая позиция мыши: {current_position}")
