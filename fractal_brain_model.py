#!/usr/bin/env python3
"""
FRACTAL HARMONIC BRAIN MODEL
Advanced Nonlinear Coupled Oscillator System with Stochastic Forcing

Based on the Fractal Harmonic Code by Adam Lee Hatchett
Fundamental Law: f₁:f₂:f₃ = n₁:n₂:n₃

This model simulates brain wave dynamics using triadic harmonic oscillators
with nonlinear coupling and stochastic noise, representing:
- Gamma waves (40 Hz): Fast cognition, attention, consciousness
- Beta waves (20 Hz): Active thinking, problem solving
- Alpha waves (10 Hz): Relaxed awareness, meditation

© 2024 Adam Lee Hatchett
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import welch
import matplotlib.pyplot as plt

def fractal_noise(n_points, exponent=1.0):
    """
    Generate 1/f^β noise (true fractal scaling).
    
    This produces pink noise (β=1), brown noise (β=2), or white noise (β=0).
    Fractal noise exhibits self-similarity across scales - a fundamental
    property of the Fractal Harmonic Code.
    
    Args:
        n_points: Number of time points
        exponent: Spectral exponent β (1.0 = pink noise, typical in nature)
    
    Returns:
        noise: Normalized fractal noise array
    """
    freqs = np.fft.fftfreq(n_points)
    spectrum = np.abs(freqs) ** (-exponent/2)
    spectrum[0] = 0  # Remove DC component
    phases = np.random.rand(n_points) * 2*np.pi
    noise = np.fft.ifft(spectrum * np.exp(1j*phases)).real
    return noise / np.std(noise)  # Normalize


def fractal_brain(t, A, params):
    """
    Triadic harmonic brain model with nonlinear coupling.
    
    Differential equations:
    dA₁/dt = -γ₁A₁ + α₁₂A₂ + α₁₃A₃ + β₁A₂A₃ + σ₁ξ₁(t)
    dA₂/dt = -γ₂A₂ + α₂₁A₁ - α₂₃A₃ + β₂A₁A₃ + σ₂ξ₂(t)
    dA₃/dt = -γ₃A₃ - α₃₁A₁ - α₃₂A₂ + β₃A₁A₂ + σ₃ξ₃(t)
    
    Parameters:
    - γ: Damping coefficients (natural frequency × 2π)
    - α: Linear coupling strengths (energy transfer between layers)
    - β: Nonlinear coupling strengths (multiplicative interactions)
    - σ: Stochastic noise amplitudes
    - ξ: White noise (Gaussian random process)
    
    Args:
        t: Time
        A: State vector [A1, A2, A3] (amplitudes of three harmonic layers)
        params: Parameter vector [γ₁,γ₂,γ₃, α₁₂,α₁₃,α₂₁,α₂₃,α₃₁,α₃₂, β₁,β₂,β₃, σ₁,σ₂,σ₃]
    
    Returns:
        [dA1/dt, dA2/dt, dA3/dt]
    """
    A1, A2, A3 = A
    g1, g2, g3, a12, a13, a21, a23, a31, a32, b1, b2, b3, s1, s2, s3 = params
    
    # Triadic coupled oscillator equations
    dA1 = -g1*A1 + a12*A2 + a13*A3 + b1*A2*A3 + s1*np.random.randn()
    dA2 = -g2*A2 + a21*A1 - a23*A3 + b2*A1*A3 + s2*np.random.randn()
    dA3 = -g3*A3 - a31*A1 - a32*A2 + b3*A1*A2 + s3*np.random.randn()
    
    return [dA1, dA2, dA3]


def fractal_brain_with_noise(t, A, params, noise1, noise2, noise3):
    """
    Triadic harmonic brain model with FRACTAL noise (1/f^β scaling).
    
    This version uses pre-generated fractal noise instead of white noise,
    producing more realistic brain dynamics with self-similar fluctuations
    across time scales.
    
    Args:
        t: Time
        A: State vector [A1, A2, A3]
        params: Parameter vector
        noise1, noise2, noise3: Pre-generated fractal noise arrays
    
    Returns:
        [dA1/dt, dA2/dt, dA3/dt]
    """
    A1, A2, A3 = A
    g1, g2, g3, a12, a13, a21, a23, a31, a32, b1, b2, b3, s1, s2, s3 = params
    
    # Get fractal noise at this time index (1000 Hz sampling)
    # Use min to avoid index overflow instead of expensive modulo
    idx = min(int(t * 1000), len(noise1) - 1)
    
    # Triadic coupled oscillator equations with fractal noise
    dA1 = -g1*A1 + a12*A2 + a13*A3 + b1*A2*A3 + s1*noise1[idx]
    dA2 = -g2*A2 + a21*A1 - a23*A3 + b2*A1*A3 + s2*noise2[idx]
    dA3 = -g3*A3 - a31*A1 - a32*A2 + b3*A1*A2 + s3*noise3[idx]
    
    return [dA1, dA2, dA3]


def simulate_brain(duration=2.0, initial_state=[1, 1, 1], params=None):
    """
    Simulate the fractal brain model.
    
    Args:
        duration: Simulation time in seconds
        initial_state: Initial amplitudes [A1, A2, A3]
        params: Model parameters (uses defaults if None)
    
    Returns:
        sol: Solution object from solve_ivp
    """
    if params is None:
        # Default parameters (brain wave frequencies)
        params = [
            40*np.pi, 20*np.pi, 10*np.pi,  # γ: Gamma (40Hz), Beta (20Hz), Alpha (10Hz)
            0.5, 0.25,                       # α₁₂, α₁₃: Gamma coupling
            -0.5, 0.25,                      # α₂₁, α₂₃: Beta coupling
            -0.25, -0.25,                    # α₃₁, α₃₂: Alpha coupling
            0.2, 0.2, 0.2,                   # β: Nonlinear coupling
            0.3, 0.3, 0.3                    # σ: Stochastic noise
        ]
    
    t_span = [0, duration]
    sol = solve_ivp(
        fractal_brain, 
        t_span, 
        initial_state, 
        args=(params,), 
        max_step=0.01,  # Increased from 0.001 for better performance
        method='RK45'
    )
    
    return sol


def simulate_brain_fractal(duration=2.0, initial_state=[1.0, 0.5, 0.2], params=None, noise_exponents=[1.0, 0.8, 1.2]):
    """
    Simulate the fractal brain model with 1/f^β noise.
    
    Args:
        duration: Simulation time in seconds
        initial_state: Initial amplitudes [A1, A2, A3]
        params: Model parameters (uses defaults if None)
        noise_exponents: Fractal exponents for each layer [β1, β2, β3]
    
    Returns:
        sol: Solution object from solve_ivp
        noise_arrays: Tuple of (noise1, noise2, noise3) for analysis
    """
    if params is None:
        # Default parameters (brain wave frequencies)
        params = [
            40*np.pi, 20*np.pi, 10*np.pi,  # γ: Gamma (40Hz), Beta (20Hz), Alpha (10Hz)
            0.5, 0.25,                       # α₁₂, α₁₃: Gamma coupling
            -0.5, 0.25,                      # α₂₁, α₂₃: Beta coupling
            -0.25, -0.25,                    # α₃₁, α₃₂: Alpha coupling
            0.2, 0.2, 0.2,                   # β: Nonlinear coupling
            0.3, 0.3, 0.3                    # σ: Stochastic noise
        ]
    
    # Generate fractal noise (1000 Hz sampling)
    np.random.seed(42)
    n_noise = int(duration * 1000)
    noise1 = fractal_noise(n_noise, exponent=noise_exponents[0])
    noise2 = fractal_noise(n_noise, exponent=noise_exponents[1])
    noise3 = fractal_noise(n_noise, exponent=noise_exponents[2])
    
    # Simulate
    t_span = [0, duration]
    t_eval = np.linspace(0, duration, n_noise)
    sol = solve_ivp(
        lambda t, Y: fractal_brain_with_noise(t, Y, params, noise1, noise2, noise3),
        t_span,
        initial_state,
        t_eval=t_eval,
        max_step=0.01,  # Increased from 0.001 for better performance
        method='RK45'
    )
    
    return sol, (noise1, noise2, noise3)


def plot_brain_waves(sol):
    """
    Plot the three harmonic brain wave layers.
    
    Args:
        sol: Solution object from simulate_brain()
    """
    plt.figure(figsize=(12, 6))
    
    plt.plot(sol.t, sol.y[0], label='Gamma (40 Hz) - Fast Cognition', linewidth=1.5)
    plt.plot(sol.t, sol.y[1], label='Beta (20 Hz) - Active Thinking', linewidth=1.5)
    plt.plot(sol.t, sol.y[2], label='Alpha (10 Hz) - Relaxed Awareness', linewidth=1.5)
    
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Amplitude', fontsize=12)
    plt.title('Fractal Harmonic Brain Model - Triadic Oscillator Dynamics', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt


def plot_phase_space(sol):
    """
    Plot 3D phase space trajectory.
    
    Args:
        sol: Solution object from simulate_brain()
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(sol.y[0], sol.y[1], sol.y[2], linewidth=0.5, alpha=0.7)
    ax.scatter(sol.y[0][0], sol.y[1][0], sol.y[2][0], c='green', s=100, label='Start')
    ax.scatter(sol.y[0][-1], sol.y[1][-1], sol.y[2][-1], c='red', s=100, label='End')
    
    ax.set_xlabel('Gamma (A₁)', fontsize=12)
    ax.set_ylabel('Beta (A₂)', fontsize=12)
    ax.set_zlabel('Alpha (A₃)', fontsize=12)
    ax.set_title('Phase Space Trajectory - Triadic Harmonic Consciousness', fontsize=14, fontweight='bold')
    ax.legend()
    
    return plt


def calculate_resonance(sol):
    """
    Calculate harmonic resonance over time.
    
    R = √(A₁² + A₂² + A₃²) / √3
    
    Args:
        sol: Solution object from simulate_brain()
    
    Returns:
        resonance: Array of resonance values
    """
    resonance = np.sqrt(sol.y[0]**2 + sol.y[1]**2 + sol.y[2]**2) / np.sqrt(3)
    return resonance


def calculate_coherence(sol):
    """
    Calculate phase coherence over time.
    
    Simplified coherence based on amplitude correlation.
    
    Args:
        sol: Solution object from simulate_brain()
    
    Returns:
        coherence: Array of coherence values
    """
    # Simplified coherence: inverse of amplitude variance
    variance = np.var([sol.y[0], sol.y[1], sol.y[2]], axis=0)
    coherence = 1.0 / (1.0 + variance)
    return coherence


def plot_power_spectrum(sol, sampling_rate=1000):
    """
    Plot power spectrum showing 1/f background + harmonic peaks.
    
    This reveals the fractal nature of the brain dynamics:
    - 1/f^β background (pink noise)
    - Sharp peaks at harmonic frequencies (40, 20, 10 Hz)
    
    Args:
        sol: Solution object from simulate_brain_fractal()
        sampling_rate: Sampling rate in Hz
    
    Returns:
        plt: Matplotlib pyplot object
    """
    # Calculate power spectral density using Welch's method
    # Increased nperseg for better performance with longer signals
    nperseg_size = min(512, len(sol.y[0]) // 4)
    f1, P1 = welch(sol.y[0], fs=sampling_rate, nperseg=nperseg_size)
    f2, P2 = welch(sol.y[1], fs=sampling_rate, nperseg=nperseg_size)
    f3, P3 = welch(sol.y[2], fs=sampling_rate, nperseg=nperseg_size)
    
    plt.figure(figsize=(12, 6))
    
    # Log-log plot to show fractal scaling
    plt.loglog(f1, P1, 'r-', linewidth=1.5, label='Gamma (40 Hz)', alpha=0.8)
    plt.loglog(f2, P2, 'g-', linewidth=1.5, label='Beta (20 Hz)', alpha=0.8)
    plt.loglog(f3, P3, 'b-', linewidth=1.5, label='Alpha (10 Hz)', alpha=0.8)
    
    # Mark harmonic frequencies
    plt.axvline(40, color='r', linestyle='--', alpha=0.5, linewidth=2)
    plt.axvline(20, color='g', linestyle='--', alpha=0.5, linewidth=2)
    plt.axvline(10, color='b', linestyle='--', alpha=0.5, linewidth=2)
    
    plt.xlabel('Frequency (Hz)', fontsize=12)
    plt.ylabel('Power Spectral Density', fontsize=12)
    plt.title('Power Spectrum: 1/f Fractal Background + Harmonic Peaks', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    
    return plt


if __name__ == "__main__":
    print("=" * 70)
    print("FRACTAL HARMONIC BRAIN MODEL")
    print("By Adam Lee Hatchett")
    print("=" * 70)
    print()
    print("Simulating triadic brain wave dynamics with FRACTAL NOISE...")
    print("- Gamma (40 Hz): Fast cognition")
    print("- Beta (20 Hz): Active thinking")
    print("- Alpha (10 Hz): Relaxed awareness")
    print()
    print("Noise characteristics:")
    print("- 1/f^1.0 (pink noise) for Gamma")
    print("- 1/f^0.8 for Beta")
    print("- 1/f^1.2 (browner noise) for Alpha")
    print()
    
    # Run simulation with fractal noise
    sol, (noise1, noise2, noise3) = simulate_brain_fractal(duration=2.0)
    
    # Calculate metrics
    resonance = calculate_resonance(sol)
    coherence = calculate_coherence(sol)
    
    print(f"Simulation complete!")
    print(f"Time points: {len(sol.t)}")
    print(f"Average Resonance: {np.mean(resonance):.3f}")
    print(f"Average Coherence: {np.mean(coherence):.3f}")
    print()
    
    # Plot results
    print("Generating plots...")
    
    plot_brain_waves(sol)
    plt.savefig('brain_waves_fractal.png', dpi=150)
    print("✓ Saved: brain_waves_fractal.png")
    
    plot_phase_space(sol)
    plt.savefig('phase_space_fractal.png', dpi=150)
    print("✓ Saved: phase_space_fractal.png")
    
    plot_power_spectrum(sol)
    plt.savefig('power_spectrum.png', dpi=150)
    print("✓ Saved: power_spectrum.png")
    print("  (Shows 1/f fractal background + harmonic peaks at 10, 20, 40 Hz)")
    
    plt.show()
    
    print()
    print("=" * 70)
    print("FRACTAL HARMONIC CODE: f₁:f₂:f₃ = n₁:n₂:n₃")
    print("Reality is HARMONIC at ALL scales")
    print("1/f noise + discrete harmonics = TRUE fractal consciousness")
    print("=" * 70)
