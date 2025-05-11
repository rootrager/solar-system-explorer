import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox

# Load the dataset
data = pd.read_csv("planets_updated.csv")

# Add atmosphere suitability
data["Atmosphere Suitability"] = data["Atmospheric Composition"].apply(lambda x: 1 if "Oxygen" in str(x) else 0)
data.fillna(0, inplace=True)

# Convert 'Orbital Period (days)' to numeric
data["Orbital Period (days)"] = pd.to_numeric(data["Orbital Period (days)"], errors='coerce').fillna(0)

# Filter safe planets
safe_planets = data[(data["Surface Gravity(m/s^2)"] >= 5) & (data["Surface Gravity(m/s^2)"] <= 15) & 
                   (data["Mean Temperature (C)"] >= -50) & (data["Mean Temperature (C)"] <= 50) & 
                   (data["Atmosphere Suitability"] == 1)]

# Save safe planets to a file
safe_planets.to_csv("safe_planets.csv", index=False)
print("Safe planets saved to 'safe_planets.csv'")

# Class for planet analysis
class SpacePlanet:
    def __init__(self, name, gravity, temp_c, atmosphere_suitability):
        self.name = name
        self.gravity = gravity
        self.temp_c = temp_c
        self.atmosphere_suitability = atmosphere_suitability
    
    def landing_force(self, mass=1000):
        return mass * self.gravity
    
    def is_livable(self):
        return (5 <= self.gravity <= 15) and (-50 <= self.temp_c <= 50) and (self.atmosphere_suitability == 1)
    
    def report(self):
        force = self.landing_force()
        livable = self.is_livable()
        return f"Planet: {self.name}\nLanding Force: {force} N\nLivable: {'Yes' if livable else 'No'}"

# GUI
class SpaceExplorer:
    def __init__(self, root, data):
        self.root = root
        self.root.title("Solar System Mission 2025")
        self.data = data
        
        tk.Label(root, text="Enter planet name:").pack()
        self.planet_entry = tk.Entry(root)
        self.planet_entry.pack()
        
        tk.Button(root, text="Explore", command=self.explore).pack()
    
    def explore(self):
        planet_name = self.planet_entry.get()
        try:
            planet = self.data[self.data["Planet"] == planet_name].iloc[0]
            explorer = SpacePlanet(planet["Planet"], planet["Surface Gravity(m/s^2)"], planet["Mean Temperature (C)"], planet["Atmosphere Suitability"])
            messagebox.showinfo("Mission Report", explorer.report())
        except IndexError:
            messagebox.showerror("Error", "Planet not found! Please enter a valid planet name.")

# Bar plot for gravity
plt.figure(figsize=(10, 6))
sns.barplot(x="Planet", y="Surface Gravity(m/s^2)", hue="Planet", data=data)
plt.title("Gravity on Solar System Planets")
plt.xlabel("Planet")
plt.ylabel("Gravity (m/s²)")
plt.axhline(y=9.8, color="green", linestyle="--", label="Earth Gravity")
plt.legend()
plt.xticks(rotation=45)
plt.savefig("gravity_plot.png")
plt.show()

# Scatter plot for temperature vs distance
plt.figure(figsize=(10, 6))
sns.scatterplot(x="Distance from Sun (10^6 km)", y="Mean Temperature (C)", hue="Planet", size="Surface Gravity(m/s^2)", data=data)
plt.title("Temperature vs Distance from Sun")
plt.xlabel("Distance from Sun (10^6 km)")
plt.ylabel("Mean Temperature (C)")
plt.savefig("temperature_plot.png")
plt.show()

# Run the GUI
root = tk.Tk()
app = SpaceExplorer(root, data)
root.mainloop()