"""
Tests for the units module
"""
import pytest
from magrathea import units


def test_constants():
    """Test physical constants"""
    assert units.M_earth > 0
    assert units.R_earth > 0
    assert units.G > 0


def test_mass_conversions():
    """Test mass conversion functions"""
    # Earth masses to kg and back
    mass_earth = 1.0
    mass_kg = units.earth_masses_to_kg(mass_earth)
    assert abs(mass_kg - units.M_earth) < 1e-10
    
    mass_earth_back = units.kg_to_earth_masses(mass_kg)
    assert abs(mass_earth_back - mass_earth) < 1e-10


def test_radius_conversions():
    """Test radius conversion functions"""
    # Earth radii to meters and back
    radius_earth = 1.0
    radius_m = units.earth_radii_to_m(radius_earth)
    assert abs(radius_m - units.R_earth) < 1e-10
    
    radius_earth_back = units.m_to_earth_radii(radius_m)
    assert abs(radius_earth_back - radius_earth) < 1e-10


def test_jupiter_earth_conversions():
    """Test Jupiter to Earth mass conversions"""
    # 1 Jupiter mass
    mass_jup = 1.0
    mass_earth = units.jupiter_masses_to_earth_masses(mass_jup)
    assert mass_earth > 300  # Jupiter is ~318 Earth masses
    assert mass_earth < 320
    
    # Convert back
    mass_jup_back = units.earth_masses_to_jupiter_masses(mass_earth)
    assert abs(mass_jup_back - mass_jup) < 1e-10


def test_pressure_units():
    """Test pressure unit constants"""
    assert units.GPa == 1e9
    assert units.bar == 1e5
    assert units.microbar == 1e-1
