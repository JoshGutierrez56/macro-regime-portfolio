import sys,unittest
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from execution import portfolio,schedule
from rule import target

class PublicEvidence(unittest.TestCase):
 def test_snapshot_arithmetic(self):
  d=pd.read_csv(ROOT/'data/research_snapshot.csv')
  self.assertEqual(len(d),368)
  self.assertEqual(len(d.groupby(['Sample','Cost_bps'])),8)
  for _,g in d.groupby(['Sample','Cost_bps']):
   g=g.sort_values('Period')
   for prefix in ['Rule','Static']:
    w=100*np.cumprod(1+g[prefix+'_return_pct'].to_numpy()/100)
    np.testing.assert_allclose(w,g[prefix+'_wealth'],atol=1e-6,rtol=0)
    draw=100*(w/np.maximum.accumulate(np.r_[100,w])[1:]-1)
    np.testing.assert_allclose(draw,g[prefix+'_drawdown_pct'],atol=1e-6,rtol=0)
   np.testing.assert_allclose(g.Rule_return_pct-g.Static_return_pct,g.Active_return_pp,atol=2e-8,rtol=0)
 def test_paper_ir(self):
  d=pd.read_csv(ROOT/'data/research_snapshot.csv')
  for sample,expected in [('Validation',1.06),('Final evaluation',-.48)]:
   a=d[(d.Sample==sample)&(d.Cost_bps==10)].Active_return_pp
   self.assertAlmostEqual(np.sqrt(12)*a.mean()/a.std(ddof=1),expected,delta=.005)
 def test_entry_cost(self):
  i=pd.date_range('2020-01-01',periods=2,tz='UTC')
  p=pd.DataFrame({'A':[100,110]},index=i);w=pd.DataFrame({'A':[1.,1.]},index=i)
  r=portfolio(p,w,10)
  self.assertAlmostEqual(r.net_return.iloc[0],1.1/1.001-1,places=12)
 def test_strict_later_execution(self):
  i=pd.date_range('2020-01-01',periods=3,tz='UTC')
  p=pd.DataFrame({'A':[100,101,102]},index=i)
  self.assertEqual(schedule(p,[i[0]]).index[0],i[1])
 def test_rule_direction_and_missing(self):
  b={'SPY':.30,'EFA':.15,'EEM':.05,'IEF':.25,'TIP':.10,'GLD':.10,'BIL':.05}
  for row,signal,equity in [({'CPATAX_yoy':1,'WALCL_yoy':1,'NFCI_level':-1},'risk_on',.6),({'CPATAX_yoy':-1,'WALCL_yoy':-1,'NFCI_level':1},'risk_off',.4),({},'missing_inputs',.5)]:
   w,s=target(row,b);self.assertEqual(s,signal);self.assertAlmostEqual(sum(w.values()),1);self.assertAlmostEqual(sum(w[k] for k in ['SPY','EFA','EEM']),equity)
if __name__=='__main__':unittest.main()
