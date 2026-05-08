"""
MAGRATHEA - Planet Interior Structure Code

A 1D planet structure code that integrates the hydrostatic equation
to compute the internal structure of differentiated planets.

Example
-------
>>> import magrathea as mag
>>> planet = mag.Planet()
>>> planet.add_layer('core', mass=0.33)
>>> planet.add_layer('mantle', mass=0.67)
>>> planet.surface_temp = 300
>>> planet.solve()
>>> print(f"Planet radius: {planet.radius:.3f} Earth radii")

Classes
-------
Planet : Main class for creating and solving planetary structures
Layer : Represents a compositional layer in a planet
Results : Container for planetary structure results

Functions
---------
load_results : Load results from a Magrathea output file
"""

__version__ = "2.0.0"
__author__ = "Chenliang Huang, David R. Rice, Jason H. Steffen"

from .planet import Planet, Layer
from .results import Results, load_results
from .config import Config, RunMode
from . import units
from . import eos

__all__ = [
    'Planet',
    'Layer',
    'Results',
    'load_results',
    'Config',
    'RunMode',
    'units',
    'eos',
    '__version__',
]
