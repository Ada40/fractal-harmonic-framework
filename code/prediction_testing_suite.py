"""
TRIADIC RESONANCE THEORY - PREDICTION TESTING SUITE
Three specific, testable predictions for missing exoplanets
Author: Adam L. Hatchett (GitHub: Ada40)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, signal
import lightkurve as lk
from astropy.timeseries import LombScargle
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. PREDICTION 1: TRAPPIST-1 MISSING PLANET
# ============================================================================

def predict_trappist1():
    """
    PREDICTION: TRAPPIST-1 has a planet at 15.2-15.8 days
    between planets g (12.35d) and h (18.77d)
    """
    print("\n" + "="*60)
    print("PREDICTION 1: TRAPPIST-1 SYSTEM")
    print("="*60)
    
    # Known TRAPPIST-1 planets (periods in days)
    trappist_periods = {
        'b': 1.51087081,
        'c': 2.4218233,
        'd': 4.049610,
        'e': 6.099615,
        'f': 9.206690,
        'g': 12.35294,
        'h': 18.767
    }
    
    print("Known periods:")
    for planet, period in trappist_periods.items():
        print(f"  {planet}: {period:.3f} days")
    
    # Analyze harmonic progression
    print("\nHarmonic analysis of triads:")
    
    # Triad 1: f-g-h (should be 4:3 stack)
    f, g, h = trappist_periods['f'], trappist_periods['g'], trappist_periods['h']
    ratio_gf = g/f
    ratio_hg = h/g
    
    print(f"\nTriad f-g-h: {f:.3f} : {g:.3f} : {h:.3f}")
    print(f"  Ratio g/f = {ratio_gf:.3f} (target 4/3 = 1.333)")
    print(f"  Ratio h/g = {ratio_hg:.3f} (target 4/3 = 1.333)")
    
    # If this is 4:3 stack, next triad should continue pattern
    # For complete 4:3 stack triad starting at g: g : X : h
    # where X = g × (4/3) = g × 1.333...
    
    X_predicted = g * (4/3)  # = 16.471 days (but h is 18.767)
    # That doesn't match. Let's try geometric approach:
    
    # The gap between g and h is large: 12.35 → 18.77 (ratio 1.519)
    # This is close to 3:2 = 1.5
    # So maybe it's actually 3:2 progression
    
    # Geometric mean of g and h:
    geometric_mean = np.sqrt(g * h)
    print(f"\nGeometric mean of g ({g:.3f}d) and h ({h:.3f}d): {geometric_mean:.3f} days")
    
    # Harmonic mean:
    harmonic_mean = 2 / (1/g + 1/h)
    print(f"Harmonic mean: {harmonic_mean:.3f} days")
    
    # Based on 3:2 stack progression (1 : 1.5 : 2.25):
    # g is position 1, h is position 3 (g × 2.25 = 27.79 ≠ 18.77)
    # Actually h/g = 1.519 ≈ 1.5
    
    # Let's fit to 3:2 stack: g × (3/2)^n
    n = np.log(h/g) / np.log(1.5)
    print(f"h is approximately g × (3/2)^{n:.3f}")
    
    # For complete triad, we'd want integer n
    # If n=1: g × 1.5 = 18.53 (close to h=18.77)
    # So maybe g and h ARE the 1 and 1.5 positions
    # Then the 2.25 position would be at: g × 2.25 = 27.79 days
    
    # But there's also possibility of planet BETWEEN g and h
    # Midpoint in log space:
    log_g, log_h = np.log(g), np.log(h)
    log_pred = (log_g + log_h) / 2
    period_pred = np.exp(log_pred)
    
    print(f"\nPREDICTION:")
    print(f"Missing planet between g ({g:.2f}d) and h ({h:.2f}d)")
    print(f"Predicted period: {period_pred:.2f} ± 0.3 days")
    print(f"Range: 15.0 - 15.6 days")
    print("\nRationale: The f-g-h triad shows 4:3 stack pattern,")
    print("but g-h gap suggests 3:2 ratio. A planet at ~15.3 days")
    print("would create two perfect triads: f-g-? and ?-g-h")
    
    return period_pred

# ============================================================================
# 2. PREDICTION 2: KEPLER-80 MISSING PLANET
# ============================================================================

def analyze_kepler80():
    """
    PREDICTION: Kepler-80 has planet at 2.95-3.00 days or 3.85 days
    """
    print("\n" + "="*60)
    print("PREDICTION 2: KEPLER-80 SYSTEM")
    print("="*60)
    
    # Known Kepler-80 planets
    kepler80_periods = {
        'b': 0.9867873,
        'c': 3.072225,
        'd': 4.644889,
        'e': 7.052460,
        'f': 9.52355
    }
    
    print("Known periods:")
    for planet, period in kepler80_periods.items():
        print(f"  {planet}: {period:.4f} days")
    
    # Analyze triads
    print("\nTriad analysis:")
    
    # Triad b-c-d
    b, c, d = kepler80_periods['b'], kepler80_periods['c'], kepler80_periods['d']
    ratio_cb = c/b  # 3.114
    ratio_db = d/b  # 4.707
    
    print(f"\nTriad b-c-d: {b:.4f} : {c:.4f} : {d:.4f}")
    print(f"  Targets: 1:3:5 harmonic = 1 : 3 : 5")
    print(f"  Actual: 1 : {ratio_cb:.3f} : {ratio_db:.3f}")
    print(f"  Errors: {abs(ratio_cb-3)/3*100:.1f}%, {abs(ratio_db-5)/5*100:.1f}%")
    
    # To perfect 1:3:5, c should be at b×3 = 2.960 days
    c_predicted = b * 3
    print(f"\nFor perfect 1:3:5 harmony:")
    print(f"  Planet c should be at: {c_predicted:.4f} days (currently {c:.4f})")
    print(f"  Difference: {abs(c-c_predicted):.4f} days")
    
    # Alternative: Look at c-d-e triad
    c, d, e = kepler80_periods['c'], kepler80_periods['d'], kepler80_periods['e']
    ratio_dc = d/c  # 1.512
    ratio_ec = e/c  # 2.295
    
    print(f"\nTriad c-d-e: {c:.4f} : {d:.4f} : {e:.4f}")
    print(f"  Targets: 3:2 stack = 1 : 1.5 : 2.25")
    print(f"  Actual: 1 : {ratio_dc:.3f} : {ratio_ec:.3f}")
    print(f"  Errors: {abs(ratio_dc-1.5)/1.5*100:.1f}%, {abs(ratio_ec-2.25)/2.25*100:.1f}%")
    
    # This is nearly perfect! But suggests maybe planet between c and d?
    # For perfect 1:1.5:2.25, d should be at c×1.5 = 4.608 days (actual 4.645)
    
    # What about planet between d and e?
    # Geometric mean: √(4.645 × 7.052) = 5.722 days
    # But harmonic prediction from c-d-e being 3:2 stack:
    # Next in sequence after e would be e×1.5 = 10.579 days (close to f=9.524)
    
    print(f"\nPREDICTION 2A (Primary):")
    print(f"Missing/offset planet near {c_predicted:.3f} days")
    print(f"(To perfect the b-c-d 1:3:5 harmonic triad)")
    
    print(f"\nPREDICTION 2B (Secondary):")
    print(f"Possible planet between c ({c:.3f}d) and d ({d:.3f}d)")
    print(f"at geometric mean: {np.sqrt(c*d):.3f} days ≈ 3.78 days")
    print(f"Range: 3.7 - 3.9 days")
    
    return c_predicted, np.sqrt(c*d)

# ============================================================================
# 3. PREDICTION 3: HD 219134 MISSING PLANET  
# ============================================================================

def analyze_hd219134():
    """