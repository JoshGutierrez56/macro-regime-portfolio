"""Monthly metrics; inputs must already be net of costs and aligned."""
import numpy as np
import pandas as pd

def evaluate(strategy, benchmark, cash):
    for series in [strategy,benchmark,cash]:
        if not isinstance(series,pd.Series) or not isinstance(series.index,pd.DatetimeIndex):
            raise ValueError('Dated monthly Series required')
        if series.index.has_duplicates or not series.index.is_monotonic_increasing:
            raise ValueError('Dates must be unique and increasing')
    if not strategy.index.equals(benchmark.index) or not strategy.index.equals(cash.index):
        raise ValueError('Return dates must match exactly')
    monthly=strategy.index.to_period('M')
    if monthly.has_duplicates or (len(monthly)>1 and not np.all(np.diff(monthly.asi8)==1)):
        raise ValueError('One observation per contiguous month required')
    data=np.column_stack([strategy,benchmark,cash])
    if len(data)<12 or not np.isfinite(data).all() or (data<=-1).any():
        raise ValueError('At least 12 valid monthly simple returns greater than -100% required')
    excess=strategy-cash
    active=strategy-benchmark
    def ratio(x):
        sd=x.std(ddof=1)
        return None if sd<1e-12 else float(np.sqrt(12)*x.mean()/sd)
    wealth=np.r_[1.,np.cumprod(1+strategy.to_numpy())]
    return dict(months=len(strategy),sharpe=ratio(excess),information_ratio=ratio(active),
                annualized_active_return=float(12*active.mean()),
                tracking_error=float(np.sqrt(12)*active.std(ddof=1)),
                cagr=float(wealth[-1]**(12/len(strategy))-1),
                maximum_drawdown=float(np.min(wealth/np.maximum.accumulate(wealth)-1)),
                annualization_note='Monthly sqrt(12); serial-correlation adjustment not yet implemented')
