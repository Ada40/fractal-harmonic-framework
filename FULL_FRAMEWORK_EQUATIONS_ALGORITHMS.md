# ADA40 / PULSE NINE — FULL FRAMEWORK
## Equations + Algorithms (Proof / Source-of-Record)

**Author:** Adam Lee Hatchett  
**Location:** Hampton Roads, VA  
**GitHub:** [Ada40](https://github.com/Ada40)  
**Repository:** [fractal-harmonic-framework](https://github.com/Ada40/fractal-harmonic-framework)  
**Commit purpose:** Public timestamped record of the control layer, geometry candidates, field forms, and algorithms as developed in this lineage.

**Related:** [ORIGIN_STORY.md](ORIGIN_STORY.md) · [PREDICTIONS_AND_TOYS.md](PREDICTIONS_AND_TOYS.md)

**Status:** Systems/AI layer is implementable. Physics layer is research candidates and toys — not peer-certified law.

---

## Lineage (brief)

Rat Trap adaptive switching (physical ESP32) → harmonic / rotational work → **Adam’s Harmonic Principle** → triadic law (−1/0/+1) → vorticity → pressure intuition → **Pulse Nine** → PCI / ADR → MetaDiamond stepping → pitch & lensing candidates.

---

# PART A — CORE CONTROL (AI / SOFTWARE)

## A1. Triadic state

```text
S ∈ {−1, 0, +1}
+1 Expand   : search, spawn agents, explore code paths
 0 Hold     : answer from ADR / known context only
−1 Contract : prune weak memory, refine, close expand gates
```

## A2. PCI — Pulse Coherence Index

**v1 weights are a hypothesis; log real tuples and refit.**

```text
PCI = 0.40*stability + 0.30*sync + 0.20*resonance + 0.10*fidelity
PCI ← EMA(PCI, α)
```

Concrete v1 metrics:

```text
stability  = 1 - (mode_or_tool_switches / max(1, turns_in_window))
sync       = 1 - (conflict_flags / max(1, active_items))
resonance  = |ADR_hits(query)| / max(1, |ADR_candidates|)
fidelity   = 1 - (user_corrections / max(1, claims_made))
# unmeasurable component → contribute 0.5 (neutral)
```

Bands (example):

```text
PCI < 0.50  Critical  → Hold only
0.50–0.69   Moderate  → limited tools
0.70–0.84   Good      → normal Expand
≥ 0.85      Excellent → deep agents / heavy coding
```

## A3. Gate algorithm

```text
gate(S, PCI, kind) → allow ∈ {true, false}

kind ∈ {chat, code_read, code_write, search, scrape, spawn_agent,
        adr_write, adr_prune, speak, listen}

if PCI < 0.50: allow only chat, code_read, adr_read
if S == 0:     no search, no spawn_agent, no bulk code_write
if S == +1 and PCI ≥ 0.70: allow search / spawn / code_write
if S == −1:    prefer adr_prune / refine; no expand
adr_write only if item_score ≥ WRITE_MIN (e.g. 0.70)
```

## A4. Rat Trap → software (adaptive switching)

```text
phase ∈ {COMFORT, ARMED, CAPTURE, SWITCH, RESET}
COMFORT: observe; if count ≥ T_comfort → ARMED
ARMED:   ordered pipeline stages; if threshold → SWITCH
SWITCH:  close failing strategy; open next; return COMFORT
```

Map: comfort → observe; threshold → PCI × intent ≥ τ; arm → Expand gates; doors → parse/plan/act/verify; containment → ADR survivors only.

## A5. ADR — survivor-only memory

```text
Lookup: ADR → local dictionary → gated network
write_item(x) iff score(x) ≥ WRITE_MIN
on Contract: prune score < PRUNE_MAX and low access
user correction supersedes old (correction ledger)
agents: TTL 21 or 42; dissolve; only survivors persist
```

## A6. Pulse Nine runtime loop

```text
handle_message(text):
  1. load short session turns
  2. S ← next_triadic_state()   # default: policy + hysteresis
  3. PCI ← update_pci(...)
  4. allowed ← {k | gate(S, PCI, k)}
  5. resolve terms: ADR → local → gated net
  6. intent route within allowed
  7. ADR retrieve survivors
  8. act under gates
  9. score; ADR write survivors only
 10. Contract / session end → Synthesis → high-score ADR
```

## A7. Default constants

```text
WRITE_MIN = 0.70
PRUNE_MAX = 0.40
SESSION_TURN_CAP = 20
AGENT_TTL_SHORT = 21
AGENT_TTL_LONG  = 42
RESEARCH_DEPTH  = 3
AUTONOMOUS_MODE = False
```

---

# PART B — GEOMETRY / STEPPING (MetaDiamond)

## B1. Stepping rules (author)

```text
N_s = 12          # values per side
δ_side = 3        # lag between sides
δ_L = 3           # lag between lattices
φ governs breathing period
21 governs vorticity depth
7  governs prime-lattice irregularity
```

## B2. Arm / phase count candidate

```text
N_arms = N_s / δ_side = 12 / 3 = 4
```

## B3. Logarithmic spiral

```text
r = r0 * exp(θ * tan ψ)
tan ψ = d(ln r) / dθ
```

## B4. Pitch candidate (φ³-per-turn ansatz)

```text
r_after / r_before = φ³
tan ψ = 3 * ln(φ) / (2π)
ψ = arctan(3 * ln(φ) / (2π)) ≈ 12.95°
φ = (1 + √5) / 2 ≈ 1.6180339887
```

Candidate under the φ³-per-turn breathing hypothesis; MW published pitches often ~12°–14°.

---

# PART C — FIELD / PHYSICS CANDIDATES (RESEARCH)

## C1. Triadic gradient

```text
if dP/dr > 0: State = +1
if dP/dr = 0: State =  0
if dP/dr < 0: State = −1
```

## C2. Ψ₂₁ (Fibonacci modes, schematic)

```text
Ψ₂₁(r) = Σ_{n=1}^{21} [(−1)^{n+1} / F_n] * sin(n π r / r_max)
F_n = nth Fibonacci number
```

## C3. Coupled field

```text
Ψ_coupled(r,t) =
    Ψ₂₁(r)
  * tri_smooth(t)
  * [1 + κ sin(2π t / T_φ)]
  * (1 − exp(−r / λ_Ψ))

T_φ = 21 * φ^k   # needs locked physical time unit before H(t) tests
```

## C4. Rotation curve style (candidate)

```text
v²(r) = G * M_b(r) / r  +  α² * Ψ_coupled_term(r)
```

## C5. Master field / pressure (schematic)

```text
∇²P − (1/c²) ∂²P/∂t² = −4π G * ρ_eff * φ * Ψ₂₁ * tri_smooth(t)
```

## C6. Merger effective density

```text
ρ_eff = ρ_star + η * ρ_gas
Bullet-class: η not too large (toy-dependent)
```

## C7. Lensing closures

```text
Closure A: n = 1 + ε * Ψ_coupled
Closure B: Φ_eff = −c² * χ * Ψ_coupled
α(θ) = ε * ∫ ∇_⊥ Ψ_coupled(θ, z) dz

If ρ_eff ≈ ρ_star:
  x_lens ≈ x_star
  |x_lens − x_gas| ∼ |x_star − x_gas|
```

## C8. Fractal escape (candidate)

```text
D_H ≈ 1.905 = 2 − log_φ(2)
```

---

# PART D — ALGORITHMS

## D1. update_pci

```text
raw = 0.40*stab + 0.30*sync + 0.20*res + 0.10*fid
return ema(raw)
```

## D2. next_triadic_state (default)

```text
policy + hysteresis (not Thue-Morse by default)
conflicts high or PCI falling → bias −1
intent hard and PCI high → bias +1
else → 0
```

## D3. pulse_handle

```text
S, PCI = step_control()
allowed = filter_kinds(S, PCI)
words = resolve_terms()      # ADR → local → net
intent = route(..., allowed)
ctx = adr_retrieve(...)
out = execute(intent, ctx, allowed)
adr_write(score(out))
return out
```

## D4. Lensing toy results (executed)

| Anchoring | Result |
|-----------|--------|
| Star-anchored | QUALITATIVE PASS |
| Gas-anchored | FAIL |

## D5. η scan (1D toy)

In one Gaussian setup: star-like peaks until η ≳ 2; then gas wins. Bound is model-dependent.

---

# PART E — CORE vs SOFT

**CORE:** Triadic S, PCI gate, ADR, Rat Trap switching, Pulse loop, local-first terms, short agents, 12/3 phase, pitch candidate, lensing rule, ρ_eff/η rule, toys.

**SOFT:** Lattice brand scores, brain=pentagon analogy, anyon protection without hardware, D_pulse targets, fidelity goals, mesh inventory as theory, full no-DM proof, H(t) without locked T_φ, dodecahedron satellites without catalog test.

---

# PART F — ATTRIBUTION

**Adam Lee Hatchett — Ada40 — Hampton Roads, VA**

This file is a public proof/source-of-record of the equations and algorithms of the Ada40 / Pulse Nine framework as authored in this repository lineage. Fair use and collaboration: attribute Adam Lee Hatchett / Ada40 when using this framework.

Git commit history on this repository provides the timestamp chain.
