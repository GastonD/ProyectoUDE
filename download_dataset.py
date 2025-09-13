# download_dataset.py
# Script para descargar el dataset Kagglehub

import kagglehub

# Download latest version
path = kagglehub.dataset_download("divyanshusingh369/complete-pokemon-library-32k-images-and-csv")

print("Path to dataset files:", path)