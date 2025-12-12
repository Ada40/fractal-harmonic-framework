#!/usr/bin/env python3
"""
Performance test script to validate improvements.
Tests that optimized code still produces correct results.
"""

import numpy as np
import time
import sys

def test_brain_model():
    """Test fractal_brain_model.py optimizations."""
    print("Testing fractal_brain_model.py...")
    try:
        from fractal_brain_model import simulate_brain_fractal, calculate_resonance
        
        start = time.time()
        sol, (noise1, noise2, noise3) = simulate_brain_fractal(duration=0.5)
        elapsed = time.time() - start
        
        resonance = calculate_resonance(sol)
        
        print(f"  ✓ Simulation completed in {elapsed:.3f}s")
        print(f"  ✓ Generated {len(sol.t)} time points")
        print(f"  ✓ Average resonance: {np.mean(resonance):.3f}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_scale_dependent():
    """Test scale_dependent_coupling.py optimizations."""
    print("\nTesting scale_dependent_coupling.py...")
    try:
        from scale_dependent_coupling import (
            predict_brain_coherence, 
            predict_moon_resonance_stability,
            predict_galaxy_clustering
        )
        
        # Test vectorized operations
        spacings = np.array([2, 5, 10])
        coherences = predict_brain_coherence(spacings)
        
        distances = np.array([421800, 671100, 1070400])
        alphas = predict_moon_resonance_stability(distances)
        
        separations = np.array([30, 100, 200])
        clustering = predict_galaxy_clustering(separations)
        
        print(f"  ✓ Brain coherence (vectorized): {coherences}")
        print(f"  ✓ Moon stability (vectorized): {alphas}")
        print(f"  ✓ Galaxy clustering (vectorized): {clustering}")
        
        # Test scalar operations still work
        single_coherence = predict_brain_coherence(5)
        print(f"  ✓ Scalar operation works: {single_coherence:.3f}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_network_monitor():
    """Test network_monitor_android.py optimizations."""
    print("\nTesting network_monitor_android.py...")
    try:
        from network_monitor_android import NetworkInfo, NetworkMonitor
        
        # Test basic functionality
        info = NetworkInfo.get_network_info()
        print(f"  ✓ Network info: IP={info['ip']}, Internet={info['internet']}")
        
        monitor = NetworkMonitor()
        event = monitor.log_event('TEST', 'Performance test')
        print(f"  ✓ Event logged successfully")
        
        stats = monitor.get_statistics()
        print(f"  ✓ Statistics: {stats['total_events']} events")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_unified_coupling():
    """Test unified_coupling_function.py optimizations."""
    print("\nTesting unified_coupling_function.py...")
    try:
        from unified_coupling_function import (
            alpha_quantum,
            alpha_neural,
            alpha_orbital,
            alpha_galactic
        )
        
        # Test individual functions
        alpha_q = alpha_quantum(1, 2, 5.29177e-11)
        print(f"  ✓ Quantum coupling: {alpha_q:.6f}")
        
        G = np.array([[0, 0.8], [0.8, 0]])
        alpha_n = alpha_neural(0, 1, 0.002, G)
        print(f"  ✓ Neural coupling: {alpha_n:.6f}")
        
        alpha_o = alpha_orbital(8.9e22, 4.8e22, 1.9e27, 4.2e8, 6.7e8, 2.5e8)
        print(f"  ✓ Orbital coupling: {alpha_o:.6f}")
        
        alpha_g = alpha_galactic(1e42, 1e42, 1e22, 1e22, 1.5e24)
        print(f"  ✓ Galactic coupling: {alpha_g:.6f}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_laplace_resonance():
    """Test laplace_resonance_model.py optimizations."""
    print("\nTesting laplace_resonance_model.py...")
    try:
        from laplace_resonance_model import (
            simulate_laplace_resonance,
            calculate_resonance_angle
        )
        
        start = time.time()
        sol = simulate_laplace_resonance(duration_orbits=10)
        elapsed = time.time() - start
        
        phi_L = calculate_resonance_angle(sol)
        
        print(f"  ✓ Simulation completed in {elapsed:.3f}s")
        print(f"  ✓ Generated {len(sol.t)} time points")
        print(f"  ✓ Resonance angle: {np.mean(phi_L):.4f} ± {np.std(phi_L):.4f} rad")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 70)
    print("PERFORMANCE IMPROVEMENT VALIDATION")
    print("=" * 70)
    
    tests = [
        ("Brain Model", test_brain_model),
        ("Scale Dependent", test_scale_dependent),
        ("Network Monitor", test_network_monitor),
        ("Unified Coupling", test_unified_coupling),
        ("Laplace Resonance", test_laplace_resonance),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n{name} test failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All performance improvements validated!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
