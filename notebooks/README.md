# Magrathea Python Notebooks

This directory contains Jupyter notebooks demonstrating various features and capabilities of the Magrathea Python package.

## Setup

Before running these notebooks, ensure Magrathea is installed:

```bash
# From the repository root
pip install -e .
```

Or in Google Colab (after PyPI release):

```python
!pip install magrathea
```

## Notebooks

### 1. `01_basic_planet_structure.ipynb`
Introduction to creating and solving basic planetary structures using Magrathea.
- Create a simple Earth-like planet
- Solve for internal structure
- Plot density, pressure, and temperature profiles
- Explore different layer compositions

### 2. `02_mass_radius_relationships.ipynb`
Explore mass-radius relationships for different planet types.
- Generate mass-radius curves
- Compare different compositions (rocky, icy, gas)
- Analyze how composition affects planetary radius

### 3. `03_composition_finder.ipynb`
Use the composition finder to match observed planet properties.
- Find layer masses that match observed mass and radius
- Explore degeneracies in composition
- Uncertainty analysis

## Requirements

- Python >= 3.8
- numpy
- matplotlib
- jupyter

Install notebook dependencies:

```bash
pip install notebook matplotlib
```

## Running Notebooks

### Locally

```bash
cd notebooks
jupyter notebook
```

### In Google Colab

After Magrathea is published to PyPI, you can open these notebooks directly in Colab:

1. Upload the notebook to your Google Drive
2. Open with Google Colaboratory
3. Run the installation cell: `!pip install magrathea`

## Notes

- All notebooks are self-contained with explanations
- Expected runtime: 1-5 minutes per notebook
- Results may vary slightly due to numerical tolerances
