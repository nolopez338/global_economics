"""Independent numerical checks after fit_heights.py; writes QA evidence."""
import json
import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.optimize._numdiff import approx_derivative
import fit_heights as h

if __name__=='__main__':
    R=json.loads((h.OUT/'heights_results.json').read_text())
    p=tuple(np.array(v) for v in R['parameters'])
    b=pd.read_csv(h.OUT/'heights_bootstrap.csv')
    discrepancies=[]
    for _,row in b.iterrows():
        bp=tuple(np.array([row[f'c1_{key}'],row[f'c2_{key}']]) for key in ['weight','location','scale','alpha'])
        refined=h.extrema(bp,32769)
        nm=sum(e['type']=='mode' for e in refined)
        if nm!=row.mode_count: discrepancies.append(int(row.replicate))
    t=np.array([.4,-.4,-.3,2.,.5,-.2,-3.])
    ng=approx_derivative(lambda v:h.objective(v,h.z,'sn2')[0],t).ravel()
    gradient_error=float(np.max(abs(ng-h.objective(t,h.z,'sn2')[1])))
    lo,hi=h.domain(p)
    mass=quad(lambda v:h.density(v,p),lo,hi,epsabs=1e-10,points=list(p[1]))[0]
    mean=quad(lambda v:v*h.density(v,p),lo,hi,epsabs=1e-9,points=list(p[1]))[0]
    variance=quad(lambda v:(v-mean)**2*h.density(v,p),lo,hi,epsabs=1e-8,points=list(p[1]))[0]
    clean=pd.read_csv(h.OUT/'heights_cleaned.csv')
    assert np.array_equal(clean.height_cm.to_numpy(),h.x)
    assert not discrepancies, discrepancies
    assert abs(mass-1)<1e-8
    assert abs(mean-R['mixture_mean'])<1e-7
    assert abs(variance-R['mixture_sd']**2)<1e-6
    assert np.allclose(clean.posterior_component_1+clean.posterior_component_2,1)
    qa={'bootstrap_mode_grid_check':32769,'bootstrap_mode_count_discrepancies':discrepancies,
        'density_integral':mass,'integrated_mean':mean,'integrated_variance':variance,
        'gradient_max_error':gradient_error,'cleaned_observations_exactly_equal_input':True}
    (h.OUT/'heights_validation.json').write_text(json.dumps(qa,indent=2))
    print(json.dumps(qa,indent=2))
