"""
Equation of State (EOS) phase diagrams available in Magrathea
"""

# Phase diagrams for different layers
CORE_PHASE_DIAGRAMS = {
    'Fe_default': 'Default iron core phase diagram',
    'Fe_Seager': 'Iron from Seager et al.',
    'Fe_AQUA': 'Iron from AQUA',
}

MANTLE_PHASE_DIAGRAMS = {
    'Si_default': 'Default silicate mantle phase diagram',
    'Si_Seager': 'Silicate from Seager et al.',
    'MgSiO3_perplex': 'MgSiO3 from PerpleX',
}

HYDRO_PHASE_DIAGRAMS = {
    'water_default': 'Default water/ice phase diagram',
    'water_AQUA': 'Water from AQUA',
}

ATM_PHASE_DIAGRAMS = {
    'gas_default': 'Default ideal gas atmosphere',
    'H2He_Saumon': 'H2/He from Saumon et al.',
}

def get_available_phase_diagrams(layer_type=None):
    """
    Get available phase diagrams for a layer type
    
    Parameters
    ----------
    layer_type : str or None
        Layer type: 'core', 'mantle', 'hydro', 'atm', or None for all
        
    Returns
    -------
    dict
        Dictionary of available phase diagrams
    """
    if layer_type is None:
        return {
            'core': CORE_PHASE_DIAGRAMS,
            'mantle': MANTLE_PHASE_DIAGRAMS,
            'hydro': HYDRO_PHASE_DIAGRAMS,
            'atm': ATM_PHASE_DIAGRAMS,
        }
    
    layer_map = {
        'core': CORE_PHASE_DIAGRAMS,
        'mantle': MANTLE_PHASE_DIAGRAMS,
        'hydro': HYDRO_PHASE_DIAGRAMS,
        'hydrosphere': HYDRO_PHASE_DIAGRAMS,
        'atm': ATM_PHASE_DIAGRAMS,
        'atmosphere': ATM_PHASE_DIAGRAMS,
    }
    
    return layer_map.get(layer_type.lower(), {})


def is_valid_phase_diagram(layer_type, phase_diagram):
    """
    Check if a phase diagram is valid for a layer type
    
    Parameters
    ----------
    layer_type : str
        Layer type: 'core', 'mantle', 'hydro', 'atm'
    phase_diagram : str
        Name of the phase diagram
        
    Returns
    -------
    bool
        True if valid, False otherwise
    """
    diagrams = get_available_phase_diagrams(layer_type)
    return phase_diagram in diagrams
