"""
Configuration for pytest
"""
import pytest
import sys
from pathlib import Path

# Add package to path
package_dir = Path(__file__).parent.parent / "python"
sys.path.insert(0, str(package_dir))


@pytest.fixture
def sample_planet():
    """Create a sample planet for testing"""
    import magrathea as mag
    planet = mag.Planet()
    planet.add_layer('core', mass=0.33)
    planet.add_layer('mantle', mass=0.67)
    planet.surface_temp = 300
    return planet


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory"""
    output_dir = tmp_path / "results"
    output_dir.mkdir()
    return output_dir
