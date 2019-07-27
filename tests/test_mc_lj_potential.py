"""
Unit and regression test for the mc_lj_potential package.
"""

# Import package, test suite, and other packages as needed
import mc_lj_potential
import pytest
import sys

def test_mc_lj_potential_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mc_lj_potential" in sys.modules
