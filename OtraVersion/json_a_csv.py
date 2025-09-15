import json
import pandas as pd

ENTRADA_JSON = "datos.json"
SALIDA_CSV = "salida.csv"

with open(ENTRADA_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df.to_csv(SALIDA_CSV, index=False)

print("CSV generado:", SALIDA_CSV)
