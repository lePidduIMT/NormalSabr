import pytest
from dataclasses import dataclass
from typing import List
import numpy as np
from NormalSABR import normal_volatility, alpha_root

@dataclass
class TestData:
    forward_rate: float
    strike_rate: float
    atm_volatility: float
    negative_forward_rate: float
    negative_strike: float
    time_to_maturity: float
    shift: float
    times_array: List[float]
    strikes_array: List[float]
    forwards_array: List[float]
    atm_vols_array: List[float]


@pytest.fixture
def setUp():
    forward_rate = 0.02
    strike_rate = 0.03
    atm_volatility = 0.0025
    negative_forward_rate = - forward_rate
    negative_strike = - strike_rate
    time_to_maturity = 1.25
    shift = 0.02
    times_array = list(np.linspace(0.25, 20))
    strikes_array = list(np.linspace(0.01, 0.05))
    forwards_array = list(np.linspace(0.01, 0.05))
    atm_vols_array = list(np.linspace(0.0015, 0.0045))
    return TestData(forward_rate, strike_rate, atm_volatility,
                    negative_forward_rate, negative_strike,
                    time_to_maturity, shift, times_array,
                    strikes_array, forwards_array, atm_vols_array)

def test_alpha_root_is_non_negative(setUp):
    fwd = setUp.forward_rate
    atm_fwd_vol = setUp.atm_volatility
    ttm = setUp.time_to_maturity
    beta, nu, rho = 0.5, 0.45, -0.65
    assert alpha_root(fwd, atm_fwd_vol, ttm, beta, nu, rho) >= 0

def test_vectorized_alpha_root_is_non_negative(setUp):
    fwds = setUp.forwards_array
    atm_fwd_vols = setUp.atm_vols_array
    ttms = setUp.times_array
    beta, nu, rho = 0.5, 0.45, -0.65
    alphas = alpha_root(fwds, atm_fwd_vols, ttms, beta, nu, rho)
    assert all(alphas>=0)

def test_atm_strike_volatility_is_close_to_atm_volatility(setUp):
    fwd = setUp.forward_rate
    stk = fwd
    atm_fwd_vol = setUp.atm_volatility
    ttm = setUp.time_to_maturity
    beta, nu, rho = 0.5, 0.45, -0.65
    alpha = alpha_root(fwd, atm_fwd_vol, ttm, beta, nu, rho)
    basis_point_vol = 1/normal_volatility(fwd, atm_fwd_vol, stk, ttm, alpha, beta, nu, rho)
    absolute_error = abs(basis_point_vol - atm_fwd_vol)
    assert absolute_error <= 1e-8

def test_vectorized_atm_strike_volatility_is_close_to_atm_volatility(setUp):
    fwds = setUp.forwards_array
    stks = setUp.forwards_array
    atm_fwd_vols = setUp.atm_vols_array
    ttm = setUp.times_array
    beta, nu, rho = 0.5, 0.45, -0.65
    alphas = alpha_root(fwds, atm_fwd_vols, ttm, beta, nu, rho)
    basis_point_vols = 1.0/normal_volatility(fwds, atm_fwd_vols, stks, ttm, alphas, beta, nu, rho)
    absolute_differences = np.abs(atm_fwd_vols - basis_point_vols)
    max_absolute_difference = np.max(absolute_differences)
    assert max_absolute_difference <= 1e-8

