"""
Tests for the Magrathea Python wrapper

Run with: pytest tests/
"""
import pytest
import sys
from pathlib import Path

# Add package to path for testing
package_dir = Path(__file__).parent.parent / "python"
sys.path.insert(0, str(package_dir))
