"""
Tests for the Results module
"""
import pytest
import numpy as np
from pathlib import Path
from magrathea import Results, load_results


def test_results_creation():
    """Test creating an empty Results object"""
    results = Results()
    assert results.pressure is None
    assert results.mass is None
    assert results.radius is None


def test_results_repr():
    """Test Results repr"""
    results = Results()
    assert 'Results(empty)' in repr(results)
    
    results.radius = 1.0
    results.total_mass = 1.0
    assert 'radius=1.000' in repr(results)
    assert 'mass=1.000' in repr(results)


def test_results_summary():
    """Test results summary"""
    results = Results()
    results.radius = 1.0
    results.total_mass = 1.0
    results.core_radius = 0.5
    results.pressure = np.array([100, 50, 10])
    results.mass = np.array([0.0, 0.5, 1.0])
    results.density = np.array([10, 8, 5])
    
    summary = results.summary()
    assert 'MAGRATHEA' in summary
    assert '1.0000' in summary
    assert 'Earth' in summary.lower()


def test_load_results_file_not_found():
    """Test loading non-existent file"""
    with pytest.raises(FileNotFoundError):
        load_results('nonexistent_file.txt')


def test_create_sample_results_file(tmp_path):
    """Create a sample results file for testing"""
    results_file = tmp_path / "test_results.txt"
    
    # Create sample data
    content = """# MAGRATHEA Results
# Total Radius: 1.0 Earth radii
# Core Radius: 0.5 Earth radii
# Pressure (GPa) | Mass (M_Earth) | Density (g/cm^3) | Temperature (K) | Phase
100.0 0.0 10.0 3000 1
50.0 0.5 8.0 2000 2
10.0 1.0 5.0 1000 3
"""
    results_file.write_text(content)
    
    # Test loading
    results = load_results(str(results_file))
    
    assert len(results.pressure) == 3
    assert len(results.mass) == 3
    assert len(results.density) == 3
    assert results.pressure[0] == 100.0
    assert results.mass[-1] == 1.0
    assert results.density[0] == 10.0
    
    # Check radius extraction from comment
    assert results.radius == 1.0
    assert results.core_radius == 0.5


def test_results_with_minimal_data(tmp_path):
    """Test results file with only pressure, mass, density"""
    results_file = tmp_path / "minimal.txt"
    
    content = """100.0 0.0 10.0
50.0 0.5 8.0
10.0 1.0 5.0
"""
    results_file.write_text(content)
    
    results = load_results(str(results_file))
    
    assert len(results.pressure) == 3
    assert len(results.mass) == 3
    assert len(results.density) == 3
    assert results.total_mass == 1.0


def test_compare_results():
    """Test comparing two results"""
    from magrathea.results import compare_results
    
    results1 = Results()
    results1.pressure = np.array([100, 50, 10])
    results1.mass = np.array([0.0, 0.5, 1.0])
    results1.density = np.array([10.0, 8.0, 5.0])
    
    results2 = Results()
    results2.pressure = np.array([101, 51, 11])
    results2.mass = np.array([0.0, 0.5, 1.0])
    results2.density = np.array([10.1, 8.1, 5.1])
    
    differences = compare_results(results1, results2, ['density', 'pressure'])
    
    assert 'density' in differences
    assert 'pressure' in differences
    assert differences['density'] > 0  # Should be non-zero
    assert differences['density'] < 0.02  # Should be small (~1%)
