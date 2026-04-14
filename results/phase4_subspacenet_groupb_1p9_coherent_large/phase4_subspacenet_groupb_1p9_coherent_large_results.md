# Phase 4A - Coherent SubspaceNet on Group B 2D Geometry at 1.9 Lambda

Large-sample SubspaceNet training on the Group B hardware geometry using the best classical front end found so far: spatial smoothing before LRMC.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Row pattern used for LRMC: [0, 4, 7, 8]
- Preprocessing: spatial smoothing before LRMC
- Signals: 2 coherent narrowband targets
- Snapshots: T = 200
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Dataset size: 45,000 samples
- SubspaceNet tau: 8
- Methods: SubspaceNet-ESPRIT and SubspaceNet-Root-MUSIC
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Group B @ 1.9 lambda | coherent | SS -> LRMC | 45k | ESPRIT | 0.9599 |
| Group B @ 1.9 lambda | coherent | SS -> LRMC | 45k | Root-MUSIC | 5.6715 |

The Phase 4A result is mixed, but in a very informative way.

From [`phase4_subspacenet_groupb_1p9_coherent_large_results.md`](/f:/workspace1/SubspaceNet/results/phase4_subspacenet_groupb_1p9_coherent_large/phase4_subspacenet_groupb_1p9_coherent_large_results.md) and [`summary.csv`](/f:/workspace1/SubspaceNet/results/phase4_subspacenet_groupb_1p9_coherent_large/summary.csv):

- `SubspaceNet-ESPRIT`: `0.9599°`
- `SubspaceNet-Root-MUSIC`: `5.6715°`

## Main interpretation

### 1. The large-sample training worked well for ESPRIT
This is a strong result.

For the same Group B `1.9λ` coherent setting, the best classical result we had was around:
- `SS -> LRMC + ESPRIT`: about `2.04°`

Now the learned ESPRIT head gets:
- `0.96°`

So SubspaceNet-ESPRIT is clearly learning something useful here and is beating the classical ESPRIT pipeline by a noticeable margin.

Also, the ESPRIT loss curve looks healthy:
- fast drop early
- smooth monotonic decline
- train and validation stay close
- no obvious overfitting

That is exactly what we want to see for a stable training run.

### 2. Root-MUSIC training did not converge well enough
The Root-MUSIC result is much worse:
- `5.67°`

That is not just “a little worse than ESPRIT.”
It is far worse than:
- the learned ESPRIT head
- and also worse than the best classical Group B coherent `SS -> LRMC + Root-MUSIC` result, which was about `1.80°`

So the Root-MUSIC head is currently not successful in this setting.

---

## Why Root-MUSIC training is unstable

I think there are two layers to the problem.

### A. The differentiable Root-MUSIC path is intrinsically much less stable than ESPRIT
In [`src/models.py`](/f:/workspace1/SubspaceNet/src/models.py), the differentiable Root-MUSIC head does:

1. eigendecomposition of the surrogate covariance
2. builds the noise-subspace polynomial
3. finds polynomial roots
4. sorts roots by distance to the unit circle
5. masks roots inside the unit circle
6. selects the first `M`
7. converts root phase to angle

That pipeline has several non-smooth / discontinuous operations:
- root finding
- sorting roots
- masking roots by unit-circle membership
- selecting the top `M`

Those steps are very sensitive to small perturbations in the surrogate covariance. When two roots move close to each other or switch order, the effective training target can “jump,” and the gradient becomes noisy.

That matches the loss curve you showed:
- strong oscillation
- repeated spikes in validation loss
- no clean monotonic descent
- eventual plateau at a much worse level than ESPRIT

By contrast, differentiable ESPRIT is simpler:
- eigendecomposition
- signal-subspace partition
- pseudoinverse
- eigendecomposition of `phi`
- angle extraction

It is still not trivial, but it avoids the most brittle polynomial-root-selection stage.

### B. This coherent setting makes Root-MUSIC even harder
This experiment is not an easy regime:
- coherent sources
- 2D Group B geometry
- LRMC-preprocessed virtual covariance
- narrow FOV with two close targets

Coherence makes the covariance structure more delicate. If the surrogate covariance is slightly imperfect, Root-MUSIC tends to react more sharply than ESPRIT because root locations near the unit circle are extremely sensitive.

So the coherent case amplifies exactly the weakness of the Root-MUSIC training head.

---

## There is also one code-level warning sign
In [`src/models.py`](/f:/workspace1/SubspaceNet/src/models.py), the differentiable `root_music()` still uses:

- `dist = 0.5`

That is a hardcoded half-wavelength normalization inside the learned Root-MUSIC head.

This is important.

Even though the SubspaceNet input here comes from LRMC on a virtual ULA, this hardcoded normalization is still suspicious in the current `1.9λ` experiment family. It creates an additional mismatch risk between:
- the geometry/preprocessing used to build the training input
- and the angle inversion used inside the differentiable Root-MUSIC head

ESPRIT’s differentiable head also uses a fixed-form inversion, but Root-MUSIC is much more fragile, so this kind of mismatch is more likely to hurt it badly.

So I would not treat the Root-MUSIC failure as “just optimization noise.”
There is a real chance the differentiable Root-MUSIC head is still not well matched to the current geometry/preprocessing setup.

---

## What the loss curves say

### ESPRIT curve
The ESPRIT curve looks excellent:
- train loss goes from about `0.24` down to about `0.020`
- validation goes from about `0.14` down to about `0.0175`
- validation is even slightly below training late in training, which is fine here because dropout is active in training

This is a stable, well-converged run.

### Root-MUSIC curve
The Root-MUSIC curve shows:
- very noisy early behavior
- repeated spikes throughout training
- only slow improvement after that
- train loss still around `0.20`
- validation still around `0.18`

That is not just undertraining. It looks like the optimization landscape is bad for this head.

---

## Practical conclusion

### What succeeded
- Large-sample coherent training is worthwhile for this geometry.
- SubspaceNet-ESPRIT is promising and already strong.

### What failed
- SubspaceNet-Root-MUSIC is not reliable in the current form for this task.
- The problem is likely a mix of:
  - Root-MUSIC’s inherently unstable differentiable pipeline
  - coherent-signal difficulty
  - possible normalization/model mismatch in the differentiable head

---

## Recommendation for next step

I would proceed like this:

1. Keep `SubspaceNet-ESPRIT` as the main learned model for Group B coherent `1.9λ`.
2. Do not rely on the current differentiable Root-MUSIC head for this geometry yet.
3. Before trying another large Root-MUSIC training run, inspect/fix the differentiable Root-MUSIC implementation in [`src/models.py`](/f:/workspace1/SubspaceNet/src/models.py), especially:
   - the hardcoded `dist = 0.5`
   - the discontinuous root selection logic
4. If the goal is practical performance, move on to the non-coherent Group B SubspaceNet stage with ESPRIT first.

So the clean bottom line is:

- **ESPRIT training succeeded**
- **Root-MUSIC training is currently unstable and likely structurally mismatched**
- **the best learned path forward is ESPRIT-first**

If you want, I can next do a code-level review of the differentiable Root-MUSIC head and point out exactly what should be changed before retraining it.
