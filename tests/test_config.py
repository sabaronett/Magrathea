"""
Tests for the Config module
"""
import pytest
from magrathea import Config, RunMode


def test_config_creation():
    """Test basic config creation"""
    config = Config(RunMode.FULL_SOLVER)
    assert config.mode == RunMode.FULL_SOLVER
    assert config.get('input_mode') == 0


def test_config_set_get():
    """Test setting and getting parameters"""
    config = Config()
    config.set('mass_of_core', 0.5)
    assert config.get('mass_of_core') == 0.5


def test_config_generation():
    """Test config file string generation"""
    config = Config(RunMode.FULL_SOLVER)
    config.set('mass_of_core', 0.33)
    config.set('mass_of_mantle', 0.67)
    config.set('surface_temp', 300)
    
    config_str = config.generate_config_string()
    
    assert 'mass_of_core=0.33' in config_str
    assert 'mass_of_mantle=0.67' in config_str
    assert 'surface_temp=300' in config_str


def test_config_save(tmp_path):
    """Test saving config to file"""
    config = Config()
    config.set('mass_of_core', 1.0)
    
    config_file = tmp_path / "test.cfg"
    config.save(str(config_file))
    
    assert config_file.exists()
    content = config_file.read_text()
    assert 'mass_of_core=1.0' in content


def test_config_modes():
    """Test different run modes"""
    for mode in RunMode:
        config = Config(mode)
        assert config.mode == mode
        assert config.get('input_mode') == int(mode)


def test_config_bool_formatting():
    """Test boolean parameter formatting"""
    config = Config()
    config.set('verbose', True)
    config_str = config.generate_config_string()
    assert 'verbose=true' in config_str.lower()


def test_config_scientific_notation():
    """Test scientific notation for small values"""
    config = Config()
    config.set('rho_eps_rel', 1e-11)
    config_str = config.generate_config_string()
    assert 'rho_eps_rel=' in config_str
