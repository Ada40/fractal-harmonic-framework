#!/usr/bin/env python3
"""
FRACTAL HARMONIC NEURAL OSCILLATOR MODEL
Advanced Nonlinear Coupled Oscillator System with Stochastic Forcing

Based on the Fractal Harmonic Code by Adam Lee Hatchett
Fundamental Law: f₁:f₂:f₃ = n₁:n₂:n₃

This model simulates neural oscillation dynamics using triadic harmonic oscillators
with nonlinear coupling and stochastic noise, representing standard EEG bands:
- Gamma (40 Hz): High-frequency information processing
- Beta (20 Hz): Mid-frequency cognitive task engagement
- Alpha (10 Hz): Low-frequency attentional modulation

© 2025 Adam Lee Hatchett
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import welch
import matplotlib.pyplot as plt

def fractal_noise(n_points, exponent=1.0):
    """
    Generate 1/f^β noise (Power-law spectral scaling).
    
    This produces pink noise (β=1), brown noise (β=2), or white noise (β=0).
    Fractal noise exhibits scale-invariance, a fundamental property 
    observed in biological and physical systems.
    
    Args:
        n_points: Number of time points
        exponent: Spectral exponent β (1.0 = pink noise)
    
    Returns:
        noise: Normalized fractal noise array
    """
    freqs = np.fft.fftfreq(n_points)
    # Avoid division by zero at DC component
    with np.errstate(divide='ignore'):
        spectrum = np.abs(freqs) ** (-exponent/2)
    spectrum[0] = 0  
    phases = np.random.rand(n_points) * 2*np.pi
    noise = np.fft.ifft(spectrum * np.exp(1j*phases)).real
    return noise / np.std(noise)  # Normalize

def triadic_oscillator_dynamics(t, A, params):
    """
    Triadic coupled oscillator model with nonlinear interactions.
    
    Differential equations:
    dA₁/dt = -γ₁A₁ + α₁₂A₂ + α₁₃A₃ + β₁A₂A₃ + σ₁ξ₁(t)
    dA₂/dt = -γ₂A₂ + α₂₁A₁ - α₂₃A₃ + β₂A₁A₃ + σ₂ξ₂(t)
    dA₃/dt = -γ₃A₃ - α₃₁A₁ - α₃₂A₂ + β₃A₁A₂ + σ₃ξ₃(t)
    
    Parameters:
    - γ: Damping/Frequency coefficients
    - α: Linear coupling coefficients (inter-mode energy transfer)
    - β: Nonlinear coupling coefficients (cross-frequency coupling)
    - σ: Stochastic forcing amplitudes
    - ξ: Gaussian white noise
    
    Args:
        t: Time
        A: State vector [A1, A2, A3] (mode amplitudes)
        params: Parameter vector
    
    Returns:
        [dA1/dt, dA2/dt, dA3/dt]
    """
    A1, A2, A3 = A
    g1, g2, g3, a12, a13, a21, a23, a31, a32, b1, b2, b3, s1, s2, s3 = params
    
    dA1 = -g1*A1 + a12*A2 + a13*A3 + b1*A2*A3 + s1*np.random.randn()
    dA2 = -g2*A2 + a21*A1 - a23*A3 + b2*A1*A3 + s2*np.random.randn()
    dA3 = -g3*A3 - a31*A1 - a32*A2 + b3*A1*A2 + s3*np.random.randn()
    
    return [dA1, dA2, dA3]

def simulate_neural_dynamics(duration=2.0, initial_state=[1.0, 0.5, 0.2], params=None):
    """
    Execute simulation of the triadic neural model.
    """
    if params is None:
        # Default parameters aligned with EEG band ratios (4:2:1)
        params = [
            40*np.pi, 20*np.pi, 10*np.pi,  # γ: Gamma, Beta, Alpha
            0.5, 0.25,                       # α linear coupling
            -0.5, 0.25,
            -0.25, -0.25,
            0.2, 0.2, 0.2,                   # β nonlinear coupling
            0.3, 0.3, 0.3                    # σ noise amplitude
        ]
    
    t_span = [0, duration]
    t_eval = np.linspace(0, duration, int(duration * 1000))
    sol = solve_ivp(
        triadic_oscillator_dynamics, 
        t_span, 
        initial_state, 
        args=(params,), 
        t_eval=t_eval,
        max_step=0.001,
        method='RK45'
    )
    
    return sol

def calculate_system_resonance(sol):
    """
    Calculate triadic resonance coefficient.
    R = √(A₁² + A₂² + A₃²) / √3
    """
    return np.sqrt(sol.y[0]**2 + sol.y[1]**2 + sol.y[2]**2) / np.sqrt(3)

def calculate_mode_coherence(sol):
    """
    Calculate amplitude-based coherence across modes.
    """
    variance = np.var([sol.y[0], sol.y[1], sol.y[2]], axis=0)
    return 1.0 / (1.0 + variance)

def plot_dynamics(sol):
    """
    Visualize triadic mode evolution.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(sol.t, sol.y[0], label='Gamma (40 Hz)', linewidth=1.5)
    plt.plot(sol.t, sol.y[1], label='Beta (20 Hz)', linewidth=1.5)
    plt.plot(sol.t, sol.y[2], label='Alpha (10 Hz)', linewidth=1.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Triadic Neural Oscillator Dynamics')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

if __name__ == "__main__":
    print("FRACTAL HARMONIC NEURAL OSCILLATOR MODEL")
    print("Executing simulation...")
    
    sol = simulate_neural_dynamics()
    resonance = calculate_system_resonance(sol)
    coherence = calculate_mode_coherence(sol)
    
    print(f"Simulation Complete.")
    print(f"Mean System Resonance: {np.mean(resonance):.3f}")
    print(f"Mean Mode Coherence: {np.mean(coherence):.3f}")
    
    # Save results
    plot_dynamics(sol)
    plt.savefig('neural_dynamics_analysis.png', dpi=150)
    print("Results saved to neural_dynamics_analysis.png")
