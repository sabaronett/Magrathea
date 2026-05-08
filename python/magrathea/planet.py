"""
Main Planet class for Magrathea
"""
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Union
import warnings

from .config import Config, RunMode
from .results import Results, load_results
from . import eos as eos_module


class Layer:
    """
    Represents a compositional layer in a planet
    
    Parameters
    ----------
    name : str
        Layer name ('core', 'mantle', 'hydro'/'hydrosphere', 'atm'/'atmosphere')
    mass : float
        Layer mass in Earth masses
    phase_diagram : str, optional
        Phase diagram to use for this layer
        
    Attributes
    ----------
    name : str
        Layer name
    mass : float
        Layer mass (Earth masses)
    phase_diagram : str
        Phase diagram name
    """
    
    LAYER_NAMES = {
        'core': ('core', 'Fe_default'),
        'mantle': ('mantle', 'Si_default'),
        'hydro': ('hydro', 'water_default'),
        'hydrosphere': ('hydro', 'water_default'),
        'atm': ('atm', 'gas_default'),
        'atmosphere': ('atm', 'gas_default'),
    }
    
    def __init__(self, name: str, mass: float = 0.0, phase_diagram: Optional[str] = None):
        if name.lower() not in self.LAYER_NAMES:
            raise ValueError(f"Invalid layer name: {name}. Must be one of {list(self.LAYER_NAMES.keys())}")
        
        self._internal_name, default_phase = self.LAYER_NAMES[name.lower()]
        self.name = name.lower()
        self.mass = mass
        self.phase_diagram = phase_diagram or default_phase
        
        # Validate phase diagram
        if not eos_module.is_valid_phase_diagram(self._internal_name, self.phase_diagram):
            warnings.warn(f"Phase diagram '{self.phase_diagram}' may not be valid for {self.name} layer")
    
    def __repr__(self) -> str:
        return f"Layer(name='{self.name}', mass={self.mass:.4f} M_Earth, phase='{self.phase_diagram}')"


class Planet:
    """
    Main class for creating and solving planetary interior structures
    
    This class provides a Pythonic interface to the Magrathea C++ code,
    similar to how REBOUND works.
    
    Parameters
    ----------
    mode : RunMode or int, optional
        Solver mode (default: RunMode.FULL_SOLVER)
    
    Attributes
    ----------
    mode : RunMode
        Solver mode
    layers : list of Layer
        Compositional layers
    surface_temp : float
        Surface temperature (K)
    temp_jump_1 : float
        Temperature jump between atmosphere and hydrosphere (K)
    temp_jump_2 : float
        Temperature jump between hydrosphere and mantle (K)
    temp_jump_3 : float
        Temperature jump between mantle and core (K)
    results : Results or None
        Results from last solve() call
    config : Config
        Configuration object
        
    Examples
    --------
    >>> import magrathea as mag
    >>> 
    >>> # Create an Earth-like planet
    >>> planet = mag.Planet()
    >>> planet.add_layer('core', mass=0.33)
    >>> planet.add_layer('mantle', mass=0.67)
    >>> planet.surface_temp = 300
    >>> 
    >>> # Solve for the structure
    >>> planet.solve()
    >>> 
    >>> # Access results
    >>> print(f"Radius: {planet.results.radius:.3f} R_Earth")
    >>> print(planet.results.summary())
    >>> 
    >>> # Plot
    >>> planet.results.plot('mass', 'density')
    """
    
    def __init__(self, mode: Union[RunMode, int] = RunMode.FULL_SOLVER):
        self.mode = RunMode(mode)
        self.layers: List[Layer] = []
        self.surface_temp: float = 300.0
        self.temp_jump_1: float = 0.0  # atm to hydro
        self.temp_jump_2: float = 0.0  # hydro to mantle
        self.temp_jump_3: float = 0.0  # mantle to core
        self.results: Optional[Results] = None
        self.config: Optional[Config] = None
        
        # Advanced options
        self.verbose: bool = False
        self.P_surface: float = 1e5  # microbar
        
        # Tolerances (expert use)
        self.tolerances: Dict[str, float] = {}
        
        # Path to executable (will be set when needed)
        self._executable: Optional[Path] = None
    
    def add_layer(self, name: str, mass: float, phase_diagram: Optional[str] = None) -> Layer:
        """
        Add a compositional layer to the planet
        
        Parameters
        ----------
        name : str
            Layer name ('core', 'mantle', 'hydro', 'atm')
        mass : float
            Layer mass in Earth masses
        phase_diagram : str, optional
            Phase diagram to use (uses default if not specified)
            
        Returns
        -------
        Layer
            The created layer object
            
        Examples
        --------
        >>> planet.add_layer('core', mass=0.33)
        >>> planet.add_layer('mantle', mass=0.67, phase_diagram='Si_Seager')
        """
        layer = Layer(name, mass, phase_diagram)
        
        # Remove existing layer with same name if present
        self.layers = [l for l in self.layers if l._internal_name != layer._internal_name]
        
        # Add new layer
        self.layers.append(layer)
        
        return layer
    
    def remove_layer(self, name: str) -> None:
        """Remove a layer by name"""
        layer_map = Layer.LAYER_NAMES
        if name.lower() in layer_map:
            internal_name = layer_map[name.lower()][0]
            self.layers = [l for l in self.layers if l._internal_name != internal_name]
    
    def get_layer(self, name: str) -> Optional[Layer]:
        """Get a layer by name"""
        layer_map = Layer.LAYER_NAMES
        if name.lower() in layer_map:
            internal_name = layer_map[name.lower()][0]
            for layer in self.layers:
                if layer._internal_name == internal_name:
                    return layer
        return None
    
    @property
    def total_mass(self) -> float:
        """Total planet mass (Earth masses)"""
        return sum(layer.mass for layer in self.layers)
    
    def _find_executable(self) -> Path:
        """Find the Magrathea executable"""
        if self._executable is not None and self._executable.exists():
            return self._executable
        
        # Check in package directory
        import magrathea
        package_dir = Path(magrathea.__file__).parent
        
        exe_name = 'planet.exe' if os.name == 'nt' else 'planet'
        exe_path = package_dir / exe_name
        
        if exe_path.exists():
            self._executable = exe_path
            return exe_path
        
        # Check in PATH
        exe_name = 'planet'
        for path_dir in os.environ.get('PATH', '').split(os.pathsep):
            exe_path = Path(path_dir) / exe_name
            if exe_path.exists():
                self._executable = exe_path
                return exe_path
        
        # Check in repository root (for development)
        repo_root = Path(__file__).parent.parent.parent
        exe_path = repo_root / exe_name
        if exe_path.exists():
            self._executable = exe_path
            return exe_path
        
        raise FileNotFoundError(
            "Magrathea executable not found. Please ensure the package is properly installed, "
            "or build the executable with 'make' in the repository root."
        )
    
    def _generate_config(self, output_file: str) -> Config:
        """Generate configuration for this planet"""
        config = Config(mode=self.mode, output_file=output_file)
        
        # Set layer masses
        layer_masses = {
            'core': 0.0,
            'mantle': 0.0,
            'hydro': 0.0,
            'atm': 0.0,
        }
        
        phase_diagrams = {
            'core': 'Fe_default',
            'mantle': 'Si_default',
            'hydro': 'water_default',
            'atm': 'gas_default',
        }
        
        for layer in self.layers:
            layer_masses[layer._internal_name] = layer.mass
            phase_diagrams[layer._internal_name] = layer.phase_diagram
        
        config.set('mass_of_core', layer_masses['core'])
        config.set('mass_of_mantle', layer_masses['mantle'])
        config.set('mass_of_hydro', layer_masses['hydro'])
        config.set('mass_of_atm', layer_masses['atm'])
        
        # Set phase diagrams
        if self.mode in [RunMode.FULL_SOLVER, RunMode.BULK_SOLVER, RunMode.COMPOSITION_FINDER]:
            config.set('core_phasedgm', phase_diagrams['core'])
            config.set('mantle_phasedgm', phase_diagrams['mantle'])
            config.set('hydro_phasedgm', phase_diagrams['hydro'])
            config.set('atm_phasedgm', phase_diagrams['atm'])
        
        # Set temperatures
        config.set('surface_temp', self.surface_temp)
        config.set('temp_jump_1', self.temp_jump_1)
        config.set('temp_jump_2', self.temp_jump_2)
        config.set('temp_jump_3', self.temp_jump_3)
        
        # Set other options
        config.set('verbose', self.verbose)
        config.set('P_surface', self.P_surface)
        
        # Set tolerances if provided
        for key, value in self.tolerances.items():
            config.set(key, value)
        
        self.config = config
        return config
    
    def solve(self, output_file: Optional[str] = None) -> Results:
        """
        Solve for the planetary structure
        
        Parameters
        ----------
        output_file : str, optional
            Path to save results (default: temporary file)
            
        Returns
        -------
        Results
            Results object containing the solution
            
        Raises
        ------
        RuntimeError
            If the solver fails
            
        Examples
        --------
        >>> planet.solve()
        >>> print(planet.results.summary())
        """
        # Find executable
        executable = self._find_executable()
        
        # Create temporary directory for run
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Generate config file
            if output_file is None:
                output_file = str(tmpdir_path / "output.txt")
            
            config = self._generate_config(output_file)
            config_file = tmpdir_path / "planet.cfg"
            config.save(config_file)
            
            # Create result directory if needed
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Run Magrathea
            try:
                result = subprocess.run(
                    [str(executable), str(config_file)],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=60,
                )
                
                if self.verbose:
                    print(result.stdout)
                    if result.stderr:
                        print("Stderr:", result.stderr)
                
            except subprocess.CalledProcessError as e:
                error_msg = f"Magrathea execution failed with return code {e.returncode}\n"
                error_msg += f"Stdout: {e.stdout}\n"
                error_msg += f"Stderr: {e.stderr}"
                raise RuntimeError(error_msg)
            except subprocess.TimeoutExpired:
                raise RuntimeError("Magrathea execution timed out after 60 seconds")
            
            # Parse output and extract radius information from stdout
            radius_info = self._parse_stdout_for_radii(result.stdout)
            
            # Load results
            self.results = load_results(output_file)
            
            # Update results with radius information from stdout
            if radius_info:
                self.results.radius = radius_info.get('total', self.results.radius)
                self.results.core_radius = radius_info.get('core', self.results.core_radius)
                self.results.mantle_radius = radius_info.get('mantle', self.results.mantle_radius)
                self.results.hydro_radius = radius_info.get('hydro', self.results.hydro_radius)
        
        return self.results
    
    def _parse_stdout_for_radii(self, stdout: str) -> Dict[str, float]:
        """Parse radius information from Magrathea stdout"""
        radii = {}
        
        lines = stdout.split('\n')
        for line in lines:
            line_lower = line.lower()
            if 'radius' in line_lower:
                # Try to extract radius value
                parts = line.split()
                for i, part in enumerate(parts):
                    try:
                        value = float(part)
                        # Identify which radius this is
                        if 'total' in line_lower or 'planet' in line_lower:
                            radii['total'] = value
                        elif 'core' in line_lower:
                            radii['core'] = value
                        elif 'mantle' in line_lower:
                            radii['mantle'] = value
                        elif 'hydro' in line_lower or 'water' in line_lower:
                            radii['hydro'] = value
                        break
                    except ValueError:
                        continue
        
        return radii
    
    def __repr__(self) -> str:
        layer_str = ", ".join([f"{l.name}={l.mass:.3f}" for l in self.layers])
        return f"Planet(mode={self.mode.name}, layers=[{layer_str}], M_total={self.total_mass:.3f} M_Earth)"
    
    def summary(self) -> str:
        """Return a summary of the planet configuration"""
        lines = []
        lines.append("=" * 60)
        lines.append("MAGRATHEA Planet Configuration")
        lines.append("=" * 60)
        lines.append(f"Mode:            {self.mode.name} ({int(self.mode)})")
        lines.append(f"Total Mass:      {self.total_mass:.4f} Earth masses")
        lines.append(f"Surface Temp:    {self.surface_temp:.1f} K")
        lines.append("")
        lines.append("Layers:")
        
        for layer in sorted(self.layers, key=lambda l: ['core', 'mantle', 'hydro', 'atm'].index(l._internal_name)):
            lines.append(f"  {layer.name:12s}: {layer.mass:.4f} M_Earth ({layer.phase_diagram})")
        
        if self.results is not None:
            lines.append("")
            lines.append("Last Solution:")
            if self.results.radius is not None:
                lines.append(f"  Radius:        {self.results.radius:.4f} Earth radii")
        
        lines.append("=" * 60)
        return '\n'.join(lines)
