"""
Tests for the Planet class
"""
import pytest
from magrathea import Planet, Layer, RunMode


def test_planet_creation():
    """Test basic planet creation"""
    planet = Planet()
    assert planet.mode == RunMode.FULL_SOLVER
    assert len(planet.layers) == 0
    assert planet.total_mass == 0.0


def test_add_layer():
    """Test adding layers to a planet"""
    planet = Planet()
    
    # Add core layer
    layer = planet.add_layer('core', mass=0.33)
    assert isinstance(layer, Layer)
    assert layer.mass == 0.33
    assert len(planet.layers) == 1
    
    # Add mantle layer
    planet.add_layer('mantle', mass=0.67)
    assert len(planet.layers) == 2
    assert planet.total_mass == 1.0


def test_add_layer_aliases():
    """Test layer name aliases"""
    planet = Planet()
    
    # Test hydrosphere alias
    planet.add_layer('hydro', mass=0.1)
    planet.add_layer('hydrosphere', mass=0.2)
    assert len(planet.layers) == 1  # Should replace previous
    assert planet.layers[0].mass == 0.2
    
    # Test atmosphere alias
    planet = Planet()
    planet.add_layer('atm', mass=0.01)
    planet.add_layer('atmosphere', mass=0.02)
    assert len(planet.layers) == 1
    assert planet.layers[0].mass == 0.02


def test_remove_layer():
    """Test removing layers"""
    planet = Planet()
    planet.add_layer('core', mass=0.33)
    planet.add_layer('mantle', mass=0.67)
    assert len(planet.layers) == 2
    
    planet.remove_layer('core')
    assert len(planet.layers) == 1
    assert planet.total_mass == 0.67


def test_get_layer():
    """Test getting layers by name"""
    planet = Planet()
    planet.add_layer('core', mass=0.33)
    
    layer = planet.get_layer('core')
    assert layer is not None
    assert layer.mass == 0.33
    
    # Test non-existent layer
    assert planet.get_layer('hydro') is None


def test_planet_properties():
    """Test planet properties"""
    planet = Planet()
    planet.surface_temp = 400
    planet.temp_jump_1 = 10
    planet.temp_jump_2 = 20
    planet.temp_jump_3 = 30
    planet.verbose = True
    
    assert planet.surface_temp == 400
    assert planet.temp_jump_1 == 10
    assert planet.temp_jump_2 == 20
    assert planet.temp_jump_3 == 30
    assert planet.verbose is True


def test_planet_config_generation(sample_planet):
    """Test config generation from planet"""
    config = sample_planet._generate_config('/tmp/test.txt')
    
    assert config.get('mass_of_core') == 0.33
    assert config.get('mass_of_mantle') == 0.67
    assert config.get('surface_temp') == 300


def test_planet_modes():
    """Test different planet modes"""
    for mode in RunMode:
        planet = Planet(mode=mode)
        assert planet.mode == mode


def test_planet_repr(sample_planet):
    """Test planet string representation"""
    repr_str = repr(sample_planet)
    assert 'Planet' in repr_str
    assert 'core=0.330' in repr_str
    assert 'mantle=0.670' in repr_str


def test_planet_summary(sample_planet):
    """Test planet summary"""
    summary = sample_planet.summary()
    assert 'MAGRATHEA' in summary
    assert 'core' in summary.lower()
    assert 'mantle' in summary.lower()
    assert '1.0000' in summary  # Total mass
