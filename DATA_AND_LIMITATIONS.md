# Data, reproducibility and interpretation

This release includes a frozen 368-row **derived portfolio-results snapshot**, not raw security prices, vendor downloads, CRSP/WRDS records or school documents. Two samples and four transaction-cost assumptions are included. Published results remain provisional.

The public checks reconstruct wealth, drawdown and information ratios from those saved portfolio returns. They do not independently reproduce the underlying asset returns or certify their accuracy. The source core implements signal-to-weight mapping, strictly later execution selection, drift-aware transaction costs and monthly metrics. Full end-to-end regeneration requires separately obtained source data and historical macro vintages described in the paper; it is not a one-command raw-data replication release.

Unresolved research inputs include original BIL distribution records for March 1 and September 1, 2022; official-close discrepancies for SPY July 16, 2019 and IEF July 9, 2020; older GLD comparisons and missing history/return-methodology records. Do not replace these with guessed values. The selected surviving ETF universe is not survivorship-free. Historical validation and later evaluation were examined; neither should now be sold as a fresh untouched holdout. Retrospective diagnostics are not independent confirmation, and the attribution does not establish causality.

The native Power BI report was saved/reopened and tested for sample/cost changes and signal cross-filtering. Its school workspace remains private. The public HTML companion reproduces selected frozen-snapshot views; it is **not** an embedded Power BI report or a live market feed. Cropped Power BI screenshots are provided separately without account/browser controls.

Working paper, not peer reviewed or journal accepted. No investment advice. AI assisted implementation and drafting under the author's direction, as disclosed in the manuscript.
