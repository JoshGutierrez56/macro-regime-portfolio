"""Public computational core, extracted unchanged from the frozen research source."""
import numpy as np
import pandas as pd

def target(row,base):
    values=[row.get(k,np.nan) for k in ['CPATAX_yoy','WALCL_yoy','NFCI_level']]
    w=dict(base)
    if not np.isfinite(values).all():return w,'missing_inputs'
    votes=int(values[0]>0)+int(values[1]>0)+int(values[2]<=0)
    tilt=.1 if votes==3 else -.1 if votes<=1 else 0.
    for k in ['SPY','EFA','EEM']:w[k]=base[k]*(.5+tilt)/.5
    w['IEF']-=tilt
    return w,('risk_on' if tilt>0 else 'risk_off' if tilt<0 else 'neutral')
