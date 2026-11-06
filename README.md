# Macroeconomic Signals and Tactical Asset Allocation
## Historical Evidence on Performance, Persistence, and Portfolio Risk

Joshua Gutierrez · Working paper · November 2026

A monthly macro allocation rule, evaluated with historical information cutoffs, explicit execution timing and drift-aware trading costs. The central finding is a performance reversal—not a validated trading recommendation.

- [Read the 15-page working paper](paper/working-paper.pdf)
- [Open the public interactive results companion](https://joshgutierrez56.github.io/assets/macro-regime/index.html)
- [Portfolio](https://joshgutierrez56.github.io/#project-macro-regime)
- [Data access and limitations](DATA_AND_LIMITATIONS.md)
- Native Power BI previews: [performance](figures/powerbi-performance.png), [allocation](figures/powerbi-allocation.png)

At 10 bps per traded dollar, the 2018–2021 validation information ratio was **1.06**; the later 46-period evaluation was **−0.48**. Strategy CAGR changed from 9.27% (benchmark 8.21%) to 7.32% (benchmark 7.89%). Later equity underweights contributed to the shortfall. Source-return reconciliation remains open; these are provisional historical estimates, not live performance.

### Run the public checks
```
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```
The tests verify derived-result consistency and synthetic accounting behavior. They do not resolve the source-data exceptions. Computational functions in `src/` are extracted unchanged from the research implementation; the raw acquisition pipeline and restricted/private inputs are deliberately excluded. See the paper for full methodology.

### Contents
`paper/`: approved manuscript; `figures/`: research figures and Power BI screenshots; `data/`: derived frozen results; `src/`: rule, execution and metric core; `tests/`: public reproducibility checks.

No external access to the private school Power BI workspace is implied. No credentials, private school papers or raw licensed datasets are included. No broad redistribution license is asserted over third-party inputs.
