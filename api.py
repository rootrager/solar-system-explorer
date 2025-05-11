from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# خواندن داده‌ها از فایل CSV
data = pd.read_csv("/home/miggor/Desktop/solar_system/planets_updated.csv")


@app.get("/planets")
def get_all_planets():
    return data[["Planet", "Color", "Mean Temperature (C)", "Number of Moons"]].to_dict(orient="records")


@app.get("/planets/{planet_name}")
def get_planet(planet_name: str):
    planet = data[data["Planet"].str.lower() == planet_name.lower()]
    if len(planet) == 0:
        return {"error": "Planet not found"}
    return planet.to_dict(orient="records")[0]


@app.get("/planets/weight")
def calculate_weight(mass: float, planet_name: str):
    planet = data[data["Planet"].str.lower() == planet_name.lower()]
    if len(planet) == 0:
        return {"error": "Planet not found"}
    gravity = planet["Surface Gravity(m/s^2)"].iloc[0]
    weight = mass * gravity  # وزن = جرم × جاذبه
    return {"planet": planet_name, "mass_kg": mass, "weight_newtons": weight}


@app.get("/planets/gravity_chart")
def get_gravity_chart():
    chart_data = data[["Planet", "Surface Gravity(m/s^2)"]].to_dict(orient="records")
    return chart_data


@app.get("/planets/story")
def get_story():
    with open("README.md", "r", encoding="utf-8") as file:
        story = file.read()
    return {"story": story}


@app.get("/planets/features/{planet_name}")
def get_features(planet_name: str):
    planet = data[data["Planet"].str.lower() == planet_name.lower()]
    if len(planet) == 0:
        return {"error": "Planet not found"}
    features = {
        "planet": planet_name,
        "surface_features": planet["Surface Features"].iloc[0],
        "images": [
            {"name": "Exploration View", "url": f"https://github.com/rootrager/solar-system-analysis/blob/main/20250511_1215_Solar%20System%20Majesty_simple_compose_01jtz88435eeatmczcwy8mxt1h.png"}
            
        ]
    }
    return features