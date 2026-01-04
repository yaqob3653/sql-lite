import shutil
import os

source = r"C:\Users\ايهم\.gemini\antigravity\brain\4d65f99b-a798-4940-b117-5af4b7c5ae3b\global_trade_map_futuristic_1767472540406.png"
destination = r"c:\Users\ايهم\Desktop\sql lite\static\img\supply-map.png"

try:
    shutil.copy2(source, destination)
    print(f"Successfully copied to {destination}")
except Exception as e:
    print(f"Error copying file: {e}")
