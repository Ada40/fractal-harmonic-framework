# Ada40 Predictions and Toy Results

**Author:** Adam Lee Hatchett (Ada40) — Hampton Roads, VA  
**Status:** Candidate formulas + numerical toys. Not peer-validated cosmology.

Related: [ORIGIN_STORY.md](ORIGIN_STORY.md)

---

## 1. Spiral pitch (MetaDiamond / φ breathing)

**Stepping rules (author):**
- Each side steps through 12 values
- Each side starts 3 ticks after the previous → phase lag 3/12 = 1/4
- Lattice lag 3 ticks
- φ governs breathing; 21 vorticity depth; 7 prime-lattice irregularity

**Arm count candidate:**

```text
N_arms = 12 / 3 = 4
```

**Pitch ansatz:** one full turn stacks three φ-breaths (triadic +1/0/−1):

```text
r_after / r_before = φ³
tan(ψ) = 3 ln(φ) / (2π)
ψ = arctan(3 ln(φ) / (2π)) ≈ 12.95°
```

**Observation:** Milky Way mean pitch often cited near ~13° (typical published range ~12°–14° depending on arm/tracer).

**Status:** Candidate match within ~1° of ~13° **under the φ³-per-turn hypothesis**. Not forced by 12/3 alone without that breathing rule.

---

## 2. Lensing rule

Effective index (Closure A):

```text
n = 1 + ε Ψ_coupled
```

or weak-field potential (Closure B):

```text
Φ_eff = −c² χ Ψ_coupled
```

Deflection (schematic):

```text
α ∝ ε ∫ ∇_⊥ Ψ_coupled dz
```

---

## 3. Merger / Bullet-class rule

```text
ρ_eff = ρ_star + η ρ_gas
Ψ_coupled sourced by ρ_eff (plus medium response)
```

**Requirement for Bullet-class morphology:** η not too large, so lensing tracks collisionless baryon peaks (galaxies/stars), not shocked gas.

**Qualitative prediction:**

```text
x_lens ≈ x_star
|x_lens − x_gas| ∼ |x_star − x_gas|
```

**Failure condition:** If dynamics force η large enough that Ψ follows gas, star–gas lensing offset is lost.

---

## 4. Toy results (executed)

### 4.1 2D star- vs gas-anchored

| Anchoring | Result |
|-----------|--------|
| Star-anchored Σ[Ψ] proxy | QUALITATIVE PASS — κ peaks at ±1 (stars) |
| Gas-anchored control | FAIL — κ at center (gas) |

Note: Raw oscillatory Ψ₂₁ + Laplacian on a small grid was unstable (edge peaks). Positive definite star blobs used for geometry test.

### 4.2 1D η scan (stars at ±1, gas at 0)

| η | Peaks (approx) | nearer_stars |
|---|----------------|--------------|
| 0.0 | ±1.00 | True |
| 0.1 | ±1.00 | True |
| 0.3 | ±1.00 | True |
| 0.5 | ±1.00 | True |
| 1.0 | ±0.99 | True |
| 2.0 | 0 and ~−0.98 | False |

**Toy lesson:** In this Gaussian amplitude setup, star peaks dominate until η ≳ 2. The bound is **model-dependent** (star/gas mass and width ratio), not a universal constant. Slogan “η ≪ 1” is safer for theory; this toy only breaks clearly near η ~ 2.

---

## 5. Coupled field (reference form)

```text
Ψ_coupled(r,t) = Ψ₂₁(r) · tri_smooth(t) · [1 + κ sin(2π t / T_φ)] · (1 − e^{−r/λ_Ψ})
```

T_φ = 21 φ^k still needs a locked physical time unit before H(t) oscillation tests.

---

## 6. Open (not claimed done)

- Derive η from hydro + vorticity (not a free dial)
- Ray-trace real Bullet Cluster maps; fit ε
- Extract H(t) oscillation at fixed T_φ from public data
- Dodecahedral satellite-vertex test with fixed tolerance
- Full oscillatory Ψ₂₁ as stable 2D lens kernel

---

## 7. One-line summary

**Pitch candidate ~12.95° from φ³/turn + 4-arm phase from 12/3; lensing follows Ψ; Bullet-class pass if ρ_eff stays star-weighted (η not too large); toys confirm geometry; nature tests still open.**

Adam Lee Hatchett — Ada40 — Hampton Roads, VA
