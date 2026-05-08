"""
Tests for the EOS module
"""
import pytest
from magrathea import eos


def test_phase_diagrams_exist():
    """Test that phase diagram dictionaries exist"""
    assert len(eos.CORE_PHASE_DIAGRAMS) > 0
    assert len(eos.MANTLE_PHASE_DIAGRAMS) > 0
    assert len(eos.HYDRO_PHASE_DIAGRAMS) > 0
    assert len(eos.ATM_PHASE_DIAGRAMS) > 0


def test_default_phase_diagrams():
    """Test that default phase diagrams exist"""
    assert 'Fe_default' in eos.CORE_PHASE_DIAGRAMS
    assert 'Si_default' in eos.MANTLE_PHASE_DIAGRAMS
    assert 'water_default' in eos.HYDRO_PHASE_DIAGRAMS
    assert 'gas_default' in eos.ATM_PHASE_DIAGRAMS


def test_get_available_phase_diagrams():
    """Test getting available phase diagrams"""
    # Get all
    all_diagrams = eos.get_available_phase_diagrams()
    assert 'core' in all_diagrams
    assert 'mantle' in all_diagrams
    assert 'hydro' in all_diagrams
    assert 'atm' in all_diagrams
    
    # Get specific layer
    core_diagrams = eos.get_available_phase_diagrams('core')
    assert 'Fe_default' in core_diagrams


def test_layer_type_aliases():
    """Test layer type aliases"""
    # hydrosphere = hydro
    diagrams1 = eos.get_available_phase_diagrams('hydro')
    diagrams2 = eos.get_available_phase_diagrams('hydrosphere')
    assert diagrams1 == diagrams2
    
    # atmosphere = atm
    diagrams1 = eos.get_available_phase_diagrams('atm')
    diagrams2 = eos.get_available_phase_diagrams('atmosphere')
    assert diagrams1 == diagrams2


def test_is_valid_phase_diagram():
    """Test phase diagram validation"""
    # Valid diagrams
    assert eos.is_valid_phase_diagram('core', 'Fe_default')
    assert eos.is_valid_phase_diagram('mantle', 'Si_default')
    assert eos.is_valid_phase_diagram('hydro', 'water_default')
    assert eos.is_valid_phase_diagram('atm', 'gas_default')
    
    # Invalid diagram
    assert not eos.is_valid_phase_diagram('core', 'invalid_diagram')


def test_invalid_layer_type():
    """Test invalid layer type"""
    diagrams = eos.get_available_phase_diagrams('invalid_layer')
    assert len(diagrams) == 0
