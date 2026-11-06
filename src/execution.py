"""Public computational core, extracted unchanged from the frozen research source."""
import numpy as np
import pandas as pd

def schedule(prices, cutoffs):
    if prices.index.tz is None or prices.index.has_duplicates or not prices.index.is_monotonic_increasing:
        raise ValueError('Unique sorted timezone-aware session closes required')
    if not np.isfinite(prices.to_numpy()).all() or (prices <= 0).any().any():
        raise ValueError('Complete positive price panel required')
    selected = []
    for cutoff in cutoffs:
        stamp = pd.Timestamp(cutoff)
        if stamp.tzinfo is None:
            raise ValueError('Timezone-aware cutoff required')
        eligible = prices.index[prices.index > stamp]
        if len(eligible) == 0:
            raise ValueError('Missing execution session')
        selected.append(eligible[0])
    if len(set(selected)) != len(selected) or selected != sorted(selected):
        raise ValueError('Duplicate or unordered executions')
    return prices.loc[selected]

def static_portfolio(executions, weights, cost_bps):
    targets = pd.DataFrame([weights] * len(executions), index=executions.index).reindex(columns=executions.columns,fill_value=0.)
    return portfolio(executions, targets, cost_bps)

def portfolio(executions, targets, cost_bps):
    """Exact post-cost target weights; charge buys AND sells on actual traded dollars.

    Start entirely in cash. Costs reduce NAV before the holding-period return.
    Terminal valuation is marked, not liquidated; initial entry is charged.
    """
    if not targets.index.equals(executions.index) or list(targets.columns)!=list(executions.columns):
        raise ValueError('Targets must match execution dates and assets exactly')
    all_w=targets.to_numpy(dtype=float)
    if not np.isfinite(all_w).all() or (all_w < 0).any() or not np.allclose(all_w.sum(axis=1), 1):
        raise ValueError('Long-only fully invested weights required')
    if not np.isfinite(cost_bps) or not 0 <= cost_bps <= 100:
        raise ValueError('Invalid cost')
    rate = cost_bps / 10000
    pre = np.zeros(len(executions.columns)); rows = []
    for k in range(len(executions) - 1):
        w=all_w[k]
        # Solve f = cost_rate * sum(abs((1-f)*target - pretrade)).
        fee = 0.
        for _ in range(100):
            new = rate * np.abs((1-fee)*w-pre).sum()
            if abs(new-fee) < 1e-14:
                fee = new; break
            fee = new
        gross = executions.iloc[k+1].to_numpy()/executions.iloc[k].to_numpy()-1
        portfolio_gross = float(w @ gross)
        net = (1-fee)*(1+portfolio_gross)-1
        rows.append(dict(entry=str(executions.index[k]), exit=str(executions.index[k+1]),
                         gross_return=portfolio_gross, net_return=float(net),
                         traded_nav_fraction=float(np.abs((1-fee)*w-pre).sum()),
                         cost_nav_fraction=float(fee)))
        pre = w*(1+gross)/(1+portfolio_gross)
    return pd.DataFrame(rows)
