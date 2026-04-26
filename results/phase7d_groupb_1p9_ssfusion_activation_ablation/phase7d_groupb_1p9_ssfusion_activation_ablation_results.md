# Phase 7D - Group B 1.9 Lambda SS-Fusion Activation Ablation

Phase 7D runs a single controlled activation ablation in the primary coherent hard cell, replacing the spatial SS-fusion block's `ReLU` activations with a width-controlled anti-rectifier while keeping the `3x3` SubspaceNet backbone fixed.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
- Cell: gap = 1 deg, SNR = 1 dB, T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Training scale: 45,000 samples total with 9,000 test samples
- Learned head: ESPRIT
- Controlled variable: spatial fusion activation design only

## Results

| Variant | Backbone | RMSE (deg) | Delta vs ReLU spatial fusion | Delta vs plain SS(3/3) best baseline |
| --- | --- | ---: | ---: | ---: |
| SS(2/3 x 3) -> LRMC -> anti-rectifier learned fusion | 3x3 | 0.3592 | -0.0525 | -0.0495 |

## Reference Values

| Reference | RMSE (deg) |
| --- | ---: |
| Phase 7C ReLU spatial fusion 3x3 | 0.4118 |
| Phase 7C plain SS(3/3) 3x3 best baseline | 0.4087 |
