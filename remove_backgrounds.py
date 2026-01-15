#!/usr/bin/env python3
"""
Script to remove white backgrounds from illustrations using rembg (AI-powered background removal)
"""

from rembg import remove
from PIL import Image
import os

# Image paths
images = [
    "images/illustration-satellite-field.png",
    "images/illustration-farmer.png",
    "images/illustration-3d-terrain.png"
]

print("🎨 Removiendo fondos blancos de las ilustraciones...\n")

for img_path in images:
    if not os.path.exists(img_path):
        print(f"❌ No se encontró: {img_path}")
        continue
    
    print(f"📸 Procesando: {img_path}")
    
    # Read input image
    with open(img_path, 'rb') as input_file:
        input_data = input_file.read()
    
    # Remove background using AI
    output_data = remove(input_data)
    
    # Save output with transparent background
    output_path = img_path.replace('.png', '-no-bg.png')
    with open(output_path, 'wb') as output_file:
        output_file.write(output_data)
    
    print(f"✅ Guardado: {output_path}\n")

print("🎉 ¡Proceso completado! Todas las imágenes ahora tienen fondo transparente.")
print("\nArchivos generados:")
for img_path in images:
    output_path = img_path.replace('.png', '-no-bg.png')
    print(f"  - {output_path}")
