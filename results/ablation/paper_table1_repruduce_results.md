# Paper Table I Reproduction

Experimental conditions:
- Array: ULA, 4 elements, 0.5 lambda spacing
- Signals: 2 coherent narrowband sources
- Snapshots: T = 100
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- SubspaceNet tau: 3
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| MUSIC | 24.2774 |
| Root-MUSIC | 23.5834 |
| ESPRIT | 25.5059 |
| SubspaceNet + Root-MUSIC | 8.0307 |
| SubspaceNet + ESPRIT | 3.9867 |
