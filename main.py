import requests
import pandas as pd
import joblib
from datetime import date, timedelta

model = joblib.load('model/rain_model.pkl')

# Usa o Open-Meteo para pegar os dados de hoje e de ontem
today = date.today().isoformat()
yesterday = (date.today() - timedelta(days=1)).isoformat()

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-8.09&longitude=-34.97"
    "&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min"
    ",precipitation_sum,rain_sum,precipitation_hours"
    ",shortwave_radiation_sum,wind_speed_10m_max,wind_gusts_10m_max"
    ",relative_humidity_2m_mean,dew_point_2m_mean,cloud_cover_mean"
    ",pressure_msl_mean,cloud_cover_max,cloud_cover_min"
    ",relative_humidity_2m_max,relative_humidity_2m_min,surface_pressure_mean"
    f"&start_date={yesterday}&end_date={today}"
    "&timezone=America/Sao_Paulo"
)

response = requests.get(url)
data = response.json()['daily']

df = pd.DataFrame(data)
df.columns = [
    'time', 'temp_mean', 'temp_max', 'temp_min',
    'precip_sum', 'rain_sum', 'precip_hours',
    'radiation', 'wind_speed', 'wind_gusts',
    'humidity_mean', 'dewpoint', 'cloud_cover_mean', 'pressure_msl',
    'cloud_cover_max', 'cloud_cover_min',
    'humidity_max', 'humidity_min',
    'pressure_surface'
]

# Adiciona lag para comparar dados de ontem com os de hoje
lag_cols = ['humidity_mean', 'cloud_cover_mean', 'radiation', 'pressure_msl', 'dewpoint']
for col in lag_cols:
    df[f'{col}_yesterday'] = df[col].shift(1)

today_row = df.iloc[[1]]

# Removendo colunas não usadas no treinamento
drop_cols = ['time', 'precip_sum', 'rain_sum', 'precip_hours']
today_features = today_row.drop(columns=drop_cols)

# Previsão
proba = model.predict_proba(today_features)[0][1]
prediction = model.predict(today_features)[0]

print(f"Previsão de chuva para amanhã: {proba:.1%}")
print(f"Previsão: {'🌧 Chuva' if prediction == 1 else '☀️ Nem Chuva'}")
