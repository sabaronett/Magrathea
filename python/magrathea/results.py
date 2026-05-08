"""
Results parsing and handling for Magrathea outputs
"""
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List, Tuple


class Results:
    """
    Container for Magrathea planetary structure results
    
    Attributes
    ----------
    pressure : ndarray
        Pressure profile (GPa)
    mass : ndarray
        Enclosed mass profile (Earth masses)
    density : ndarray
        Density profile (g/cm³)
    temperature : ndarray
        Temperature profile (K)
    phase : ndarray
        Phase identifier at each point
    radius : float
        Total planet radius (Earth radii)
    core_radius : float
        Core radius (Earth radii)
    mantle_radius : float
        Mantle radius (Earth radii)
    hydro_radius : float
        Hydrosphere radius (Earth radii)
    total_mass : float
        Total planet mass (Earth masses)
    metadata : dict
        Additional metadata from the run
        
    Examples
    --------
    >>> from magrathea import load_results
    >>> results = load_results('result/Structure.txt')
    >>> print(f"Planet radius: {results.radius:.3f} R_Earth")
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(results.mass, results.density)
    >>> plt.xlabel('Enclosed Mass (M_Earth)')
    >>> plt.ylabel('Density (g/cm³)')
    >>> plt.show()
    """
    
    def __init__(self):
        self.pressure: Optional[np.ndarray] = None
        self.mass: Optional[np.ndarray] = None
        self.density: Optional[np.ndarray] = None
        self.temperature: Optional[np.ndarray] = None
        self.phase: Optional[np.ndarray] = None
        self.radius: Optional[float] = None
        self.core_radius: Optional[float] = None
        self.mantle_radius: Optional[float] = None
        self.hydro_radius: Optional[float] = None
        self.total_mass: Optional[float] = None
        self.metadata: Dict = {}
    
    def __repr__(self) -> str:
        if self.radius is not None:
            return f"Results(radius={self.radius:.3f} R_Earth, mass={self.total_mass:.3f} M_Earth)"
        return "Results(empty)"
    
    def summary(self) -> str:
        """Return a summary string of the results"""
        lines = []
        lines.append("=" * 60)
        lines.append("MAGRATHEA Results Summary")
        lines.append("=" * 60)
        
        if self.total_mass is not None:
            lines.append(f"Total Mass:          {self.total_mass:.4f} Earth masses")
        if self.radius is not None:
            lines.append(f"Total Radius:        {self.radius:.4f} Earth radii")
        
        if self.core_radius is not None and self.core_radius > 0:
            lines.append(f"Core Radius:         {self.core_radius:.4f} Earth radii")
        if self.mantle_radius is not None and self.mantle_radius > 0:
            lines.append(f"Mantle Radius:       {self.mantle_radius:.4f} Earth radii")
        if self.hydro_radius is not None and self.hydro_radius > 0:
            lines.append(f"Hydrosphere Radius:  {self.hydro_radius:.4f} Earth radii")
        
        if self.pressure is not None:
            lines.append(f"\nData Points:         {len(self.pressure)}")
            lines.append(f"Central Pressure:    {self.pressure[0]:.2f} GPa")
            lines.append(f"Central Density:     {self.density[0]:.2f} g/cm³")
            if self.temperature is not None:
                lines.append(f"Central Temperature: {self.temperature[0]:.0f} K")
        
        lines.append("=" * 60)
        return '\n'.join(lines)
    
    def plot(self, x='mass', y='density', ax=None, **kwargs):
        """
        Quick plot of results
        
        Parameters
        ----------
        x : str
            X-axis variable ('mass', 'pressure', 'temperature')
        y : str
            Y-axis variable ('density', 'pressure', 'temperature')
        ax : matplotlib.axes.Axes, optional
            Axes to plot on
        **kwargs
            Additional arguments passed to plot()
            
        Returns
        -------
        ax : matplotlib.axes.Axes
            The axes object
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib is required for plotting. Install with: pip install matplotlib")
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        x_data = getattr(self, x)
        y_data = getattr(self, y)
        
        ax.plot(x_data, y_data, **kwargs)
        
        # Labels
        labels = {
            'mass': 'Enclosed Mass (M⊕)',
            'pressure': 'Pressure (GPa)',
            'density': 'Density (g/cm³)',
            'temperature': 'Temperature (K)',
        }
        
        ax.set_xlabel(labels.get(x, x))
        ax.set_ylabel(labels.get(y, y))
        ax.grid(True, alpha=0.3)
        
        return ax


def load_results(filename: str) -> Results:
    """
    Load Magrathea results from an output file
    
    Parameters
    ----------
    filename : str
        Path to the Magrathea output file
        
    Returns
    -------
    Results
        Results object containing the planetary structure data
        
    Examples
    --------
    >>> results = load_results('result/Structure.txt')
    >>> print(results.summary())
    """
    filepath = Path(filename)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Results file not found: {filepath}")
    
    results = Results()
    
    # Read the file
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Parse header information (look for radius info in comments)
    data_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#'):
            # Parse metadata from comments
            if 'radius' in line.lower():
                # Extract radius values from comment lines
                parts = line.split()
                for j, part in enumerate(parts):
                    if 'radius' in part.lower():
                        try:
                            # Try to get the number after "radius"
                            if j + 1 < len(parts):
                                val = float(parts[j + 1])
                                if 'total' in line.lower() or 'planet' in line.lower():
                                    results.radius = val
                                elif 'core' in line.lower():
                                    results.core_radius = val
                                elif 'mantle' in line.lower():
                                    results.mantle_radius = val
                                elif 'hydro' in line.lower() or 'water' in line.lower():
                                    results.hydro_radius = val
                        except (ValueError, IndexError):
                            pass
        else:
            data_start = i
            break
    
    # Parse data columns
    # Expected format: Pressure (GPa) | Mass (M_Earth) | Density (g/cm³) | Temperature (K) | Phase
    data_lines = [line.strip() for line in lines[data_start:] if line.strip() and not line.startswith('#')]
    
    if not data_lines:
        raise ValueError(f"No data found in file: {filepath}")
    
    # Parse the data
    pressure_list = []
    mass_list = []
    density_list = []
    temperature_list = []
    phase_list = []
    
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 3:
            try:
                pressure_list.append(float(parts[0]))
                mass_list.append(float(parts[1]))
                density_list.append(float(parts[2]))
                
                if len(parts) >= 4:
                    temperature_list.append(float(parts[3]))
                if len(parts) >= 5:
                    # Phase might be a string or number
                    try:
                        phase_list.append(float(parts[4]))
                    except ValueError:
                        phase_list.append(parts[4])
            except ValueError:
                continue
    
    # Convert to numpy arrays
    results.pressure = np.array(pressure_list)
    results.mass = np.array(mass_list)
    results.density = np.array(density_list)
    
    if temperature_list:
        results.temperature = np.array(temperature_list)
    if phase_list:
        results.phase = np.array(phase_list)
    
    # Set total mass if not already set
    if results.total_mass is None and len(results.mass) > 0:
        results.total_mass = results.mass[-1]
    
    # Try to infer radius from the data if not in header
    # (In a real Magrathea output, radius is typically printed separately)
    # For now, we'll leave it as None if not found in comments
    
    return results


def compare_results(results1: Results, results2: Results, 
                   variables: List[str] = ['density', 'pressure']) -> Dict[str, float]:
    """
    Compare two results objects
    
    Parameters
    ----------
    results1 : Results
        First results object
    results2 : Results
        Second results object
    variables : list of str
        Variables to compare
        
    Returns
    -------
    dict
        Dictionary of relative differences for each variable
    """
    differences = {}
    
    for var in variables:
        data1 = getattr(results1, var, None)
        data2 = getattr(results2, var, None)
        
        if data1 is not None and data2 is not None:
            # Interpolate to common mass grid if needed
            if len(data1) != len(data2):
                mass1 = results1.mass
                mass2 = results2.mass
                # Interpolate data2 to mass1 grid
                data2_interp = np.interp(mass1, mass2, data2)
                rel_diff = np.abs((data1 - data2_interp) / data1)
            else:
                rel_diff = np.abs((data1 - data2) / data1)
            
            differences[var] = np.mean(rel_diff)
    
    return differences
