import numpy as np
import matplotlib.pyplot as plt
import csv

# --- CONFIGURATION (The "Garage" Parameters) ---
# Adjust these values based on the material you buy and your printer size.
LENS_RADIUS = 50.0       # mm (Total radius of the lens)
REFRACTIVE_INDEX = 1.49  # Acrylic / PMMA / Standard Clear Resin
BASE_THICKNESS = 2.0     # mm (Minimum thickness at the very edge)
SCHWARZSCHILD_RADIUS = 10.0 # The "Optical Strength" (Effective Event Horizon size)

# --- THE MATH (From Paper 1: Gravitational Lensing as Refraction) ---
# We mimic the deflection angle alpha = 4GM / (c^2 * r)
# For a refractive analog, the slope dh/dr relates to alpha.
# Integration yields a logarithmic thickness profile: h(r) ~ -ln(r)

# Constant C determines the "gravity" strength relative to the material index
C = SCHWARZSCHILD_RADIUS / (REFRACTIVE_INDEX - 1)

def lens_profile(r):
    """Calculates thickness h at radius r to mimic Schwarzschild geometry."""
    # Prevent mathematical errors at r=0 (singularity) by clamping slightly out
    r_safe = np.maximum(r, 0.1) 
    
    # Calculate logarithmic profile
    # We set the edge thickness to BASE_THICKNESS and thicken towards the center
    h_edge = C * np.log(LENS_RADIUS)
    h = h_edge - C * np.log(r_safe) + BASE_THICKNESS
    
    # Clamp the center spike to a printable maximum height
    MAX_HEIGHT = 40.0 
    h = np.minimum(h, MAX_HEIGHT)
    
    return h

# --- GENERATE DATA ---
print("Generating Schwarzschild Lens Geometry...")

# Generate 500 points from the center (0.1mm) to the edge (50mm)
r_values = np.linspace(0.1, LENS_RADIUS, 500)
z_values = lens_profile(r_values)

# --- EXPORT TO CSV (For CAD Software) ---
filename = "lens_profile.csv"
print(f"Saving profile data to {filename}...")
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Radius_mm", "Thickness_mm"])
    for r, z in zip(r_values, z_values):
        writer.writerow([r, z])

print("Success! Import this CSV into Fusion360/SolidWorks and 'Revolve' it.")

# --- PLOT FOR VERIFICATION ---
plt.figure(figsize=(10, 6))
plt.plot(r_values, z_values, lw=2, color='blue', label='Refractive Surface')
plt.fill_between(r_values, z_values, 0, color='cyan', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='--', alpha=0.5, label='Center Axis')

plt.title(f"Schwarzschild Lens Profile (n={REFRACTIVE_INDEX})\nGravitational Analog: $R_s$={SCHWARZSCHILD_RADIUS}mm")
plt.xlabel("Radius (mm)")
plt.ylabel("Thickness (mm)")
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.gca().set_aspect('equal')

# Show the plot
plt.show()
