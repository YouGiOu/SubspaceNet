Experiment 1: Coherent Signals (Table I) – Specific numerical values
Experimental conditions
Coherent sources
T = 100 snapshots
SNR = 10 dB
ULA array
Evaluation metric: RMSPE
| 算法                           | RMSPE (°)      |
| ---------------------------- | -------------- |
| MUSIC                        | ≈ 15–20° |
| Root-MUSIC                   | ≈ 12°          |
| ESPRIT                       | ≈ 10°          |
| SPS + Root-MUSIC             | ≈ 3°           |
| CNN                          | ≈ 0.6°         |
| DA-MUSIC                     | ≈ 0.5°         |
| **SubspaceNet + MUSIC**      | ≈ 0.3°         |
| **SubspaceNet + ESPRIT**     | ≈ 0.2°         |
| **SubspaceNet + Root-MUSIC** | **≈ 0.2° **  |

Experiment 2: Coherent Sources with Extremely Few Snapshots (Table II) – Specific numerical values
Experimental conditions
M = 2 coherent sources
T = 2 snapshots (very few)
SNR = 5 dB
RMSPE metric
 | 算法                           | RMSPE (°)  |
| ---------------------------- | ---------- |
| Root-MUSIC                   | ≈ 25°      |
| ESPRIT                       | ≈ 20°      |
| SPS + Root-MUSIC             | ≈ 8°       |
| SPS + ESPRIT                 | ≈ 6°       |
| CNN                          | ≈ 2.5°     |
| DA-MUSIC                     | ≈ 1.9°     |
| **SubspaceNet + Root-MUSIC** | **≈ 0.7°** |
| **SubspaceNet + ESPRIT**     | **≈ 0.6°** |

Experiment 3: Wideband Signals (Table III) – Specific numerical values
Experimental conditions
M = 2 OFDM wideband signals
L = 500 subcarriers
Multi-sampling rate
RMSPE metric
 | 算法                           | RMSPE (°) |
| ---------------------------- | --------- |
| Narrowband MUSIC             | ≈ 9°      |
| Narrowband Root-MUSIC        | ≈ 7°      |
| Broadband MUSIC              | ≈ 3°      |
| ESPRIT                       | ≈ 6°      |
| **SubspaceNet + MUSIC**      | ≈ 0.8°    |
| **SubspaceNet + Root-MUSIC** | ≈ 0.6°    |
| **SubspaceNet + ESPRIT**     | ≈ 0.7°    |


