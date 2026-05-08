"""
Physical constants and unit conversions for Magrathea

All constants in SI units unless otherwise specified.
"""

# Mass
M_earth = 5.972e24  # kg
M_sun = 1.989e30    # kg
M_jupiter = 1.898e27  # kg

# Radius
R_earth = 6.371e6   # m
R_sun = 6.957e8     # m
R_jupiter = 6.9911e7  # m

# Other
AU = 1.496e11       # m
G = 6.674e-11       # N m^2 kg^-2

# Density (g/cm^3)
rho_earth = 5.514

# Pressure
GPa = 1e9  # Pa
bar = 1e5  # Pa
microbar = 1e-1  # Pa

def earth_masses_to_kg(m_earth):
    """Convert Earth masses to kg"""
    return m_earth * M_earth

def kg_to_earth_masses(kg):
    """Convert kg to Earth masses"""
    return kg / M_earth

def earth_radii_to_m(r_earth):
    """Convert Earth radii to meters"""
    return r_earth * R_earth

def m_to_earth_radii(m):
    """Convert meters to Earth radii"""
    return m / R_earth

def jupiter_masses_to_earth_masses(m_jup):
    """Convert Jupiter masses to Earth masses"""
    return m_jup * (M_jupiter / M_earth)

def earth_masses_to_jupiter_masses(m_earth):
    """Convert Earth masses to Jupiter masses"""
    return m_earth * (M_earth / M_jupiter)
