"""Reproduce heights analysis: python assets/data/fit_heights.py
Python >=3.11; numpy scipy pandas matplotlib. No external data or network.
All fits maximize individual-observation likelihood subject to stated bounds.
"""
from pathlib import Path
import csv, json, sys, platform, hashlib
import numpy as np
import pandas as pd
import scipy
from scipy.special import log_ndtr, logsumexp
from scipy.optimize import minimize, brentq
from scipy.stats import skewnorm, norm, kstest, cramervonmises, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
SEED=20261102
rng=np.random.default_rng(SEED)
raw=(OUT/'heights.csv').read_bytes()
txt=raw.decode('utf-8-sig')
# The sole header and one numeric field per line make delimiter immaterial.
rows=list(csv.reader(txt.splitlines(), delimiter=','))
assert rows[0]==['height_cm']
values=pd.to_numeric(pd.Series([r[0] if len(r)==1 else None for r in rows[1:]]), errors='coerce')
keep=np.isfinite(values.to_numpy(dtype=float))
x=values[keep].to_numpy(dtype=float)
n=len(x); center=x.mean(); unit=x.std(ddof=1)
z=(x-center)/unit

def moments(p):
    w,loc,scale,alpha=p
    delta=alpha/np.sqrt(1+alpha**2)
    means=loc+scale*delta*np.sqrt(2/np.pi)
    variances=scale**2*(1-2*delta**2/np.pi)
    m=np.dot(w,means)
    v=np.dot(w,variances+(means-m)**2)
    return means,np.sqrt(variances),m,np.sqrt(v)

def unpack(t, kind):
    if kind=='sn2': return np.array([t[0],1-t[0]]),np.array([t[1],t[4]]),np.exp([t[2],t[5]]),np.array([t[3],t[6]])
    if kind=='n2': return np.array([t[0],1-t[0]]),np.array([t[1],t[3]]),np.exp([t[2],t[4]]),np.zeros(2)
    return np.ones(1),np.array([t[0]]),np.exp([t[1]]),np.array([t[2]])

def objective(t, data, kind):
    w,loc,s,a=unpack(t,kind)
    zz=(data[:,None]-loc)/s
    az=a*zz
    logphi=-.5*zz**2-.5*np.log(2*np.pi)
    lp=np.log(2)-np.log(s)+logphi+log_ndtr(az)
    joint=lp+np.log(w)
    ll=logsumexp(joint,axis=1)
    resp=np.exp(joint-ll[:,None])
    mills=np.exp(-.5*az**2-.5*np.log(2*np.pi)-log_ndtr(az))
    gl=np.sum(resp*(zz-a*mills)/s,axis=0)
    gs=np.sum(resp*(-1+zz**2-az*mills),axis=0)
    ga=np.sum(resp*mills*zz,axis=0)
    if kind=='sn2': grad=[np.sum(resp[:,0]/w[0]-resp[:,1]/w[1]),gl[0],gs[0],ga[0],gl[1],gs[1],ga[1]]
    elif kind=='n2': grad=[np.sum(resp[:,0]/w[0]-resp[:,1]/w[1]),gl[0],gs[0],gl[1],gs[1]]
    else: grad=[gl[0],gs[0],ga[0]]
    return -ll.sum(),-np.array(grad)

def fit(data, kind='sn2', starts=100, floor=1., cap=20., warm=()):
    # Fixed original-data coordinates and bounds in all bootstrap refits.
    lo=(x.min()-2*np.ptp(x)-center)/unit
    hi=(x.max()+2*np.ptp(x)-center)/unit
    sb=(np.log(floor/unit),np.log(4*np.ptp(x)/unit))
    lb=(lo,hi)
    bounds=([(0.03,.97),lb,sb,(-cap,cap),lb,sb,(-cap,cap)] if kind=='sn2' else
            [(0.03,.97),lb,sb,lb,sb] if kind=='n2' else [lb,sb,(-cap,cap)])
    initial=list(warm)
    for j in range(starts):
        w=rng.uniform(.1,.9)
        # Include quantile splits, broad overlaps, narrow groups, both skew signs.
        loc=np.quantile(data,[rng.uniform(.05,.5),rng.uniform(.5,.95)])
        scales=rng.uniform(.25,1.6,2)
        a=rng.choice([-12.,-4.,0.,4.,12.],2) if j%2==0 else rng.uniform(-cap,cap,2)
        if j%3==0: loc-=scales*a/np.sqrt(1+a*a)*np.sqrt(2/np.pi)
        if kind=='sn2': t=[w,loc[0],np.log(scales[0]),a[0],loc[1],np.log(scales[1]),a[1]]
        elif kind=='n2': t=[w,loc[0],np.log(scales[0]),loc[1],np.log(scales[1])]
        else: t=[rng.uniform(-.8,.8),np.log(rng.uniform(.6,1.6)),a[0]]
        initial.append(t)
    results=[]
    for t in initial:
        t=np.array([np.clip(v,*b) for v,b in zip(t,bounds)])
        r=minimize(objective,t,args=(data,kind),jac=True,bounds=bounds,method='L-BFGS-B',
                   options={'maxiter':1500,'ftol':1e-11,'gtol':1e-6,'maxls':40})
        results.append(r)
    valid=[r for r in results if r.success and np.isfinite(r.fun)]
    if not valid: raise RuntimeError('No converged starts')
    best=min(valid,key=lambda r:r.fun)
    w,l,s,a=unpack(best.x,kind)
    p=(w,l*unit+center,s*unit,a)
    order=np.argsort(moments(p)[0]); p=tuple(v[order] for v in p)
    active=[str(i)+(' lower' if abs(v-b[0])<1e-5 else ' upper') for i,(v,b) in enumerate(zip(best.x,bounds)) if min(abs(v-b[0]),abs(v-b[1]))<1e-5]
    diag={'attempted':len(results),'converged':len(valid),'best_loglik':-best.fun-np.log(unit)*len(data),
          'within_0.01':sum(r.fun-best.fun<.01 for r in valid),'worst_converged_loglik':-max(r.fun for r in valid)-np.log(unit)*len(data),
          'active_bounds':active,'message':str(best.message),'iterations':best.nit,
          'gradient_inf':float(np.max(np.abs(best.jac))), 'all_loglik':[-r.fun-np.log(unit)*len(data) for r in results]}
    return p,best.x,diag

def density(t,p):
    w,l,s,a=p
    return np.sum(w*skewnorm.pdf(np.asarray(t)[...,None],a,loc=l,scale=s),axis=-1)
def cdf(t,p):
    w,l,s,a=p
    return np.sum(w*skewnorm.cdf(np.asarray(t)[...,None],a,loc=l,scale=s),axis=-1)
def derivative(t,p):
    w,l,s,a=p
    zz=(np.asarray(t)[...,None]-l)/s
    return np.sum(w*2/s**2*norm.pdf(zz)*(-zz*norm.cdf(a*zz)+a*norm.pdf(a*zz)),axis=-1)
def domain(p):
    w,l,s,a=p
    # Parameter-adaptive normal envelope avoids Boost extreme-skew ppf overflow.
    # SN density <= 2 * corresponding normal density, hence each excluded
    # tail is <= 2*Phi(-10), below 1.6e-23 for every component.
    low=min(x.min(),np.min(l-10*s))
    high=max(x.max(),np.max(l+10*s))
    return float(low),float(high)
def extrema(p,grid=8193):
    low,high=domain(p); xx=np.linspace(low,high,grid); d=derivative(xx,p)
    roots=[]
    for i in np.flatnonzero(d[:-1]*d[1:]<0):
        root=brentq(lambda t:derivative(t,p),xx[i],xx[i+1],xtol=1e-11)
        roots.append({'position':root,'density':float(density(root,p)), 'type':'mode' if d[i]>0 else 'valley'})
    return roots
def quantile(q,p):
    low,high=domain(p)
    return brentq(lambda v:cdf(v,p)-q,low,high,xtol=1e-11)

if __name__=='__main__':
    print('Fitting alternatives and primary model',flush=True)
    p,t,diag=fit(z,starts=160)
    sn,st,sd=fit(z,'sn1',60)
    nn,nt,nd=fit(z,'n2',100)
    normal=(np.ones(1),np.array([x.mean()]),np.array([x.std(ddof=0)]),np.zeros(1))
    models=[('Normal',normal,2,float(norm.logpdf(x,loc=x.mean(),scale=x.std(ddof=0)).sum())),('Skew-normal',sn,3,sd['best_loglik']),('Two normals',nn,5,nd['best_loglik']),('Two skew-normals',p,7,diag['best_loglik'])]
    comparison=pd.DataFrame([{'model':name,'k':k,'log_likelihood':ll,'AIC':2*k-2*ll,'BIC':k*np.log(n)-2*ll} for name,pp,k,ll in models])
    comparison.to_csv(OUT/'heights_model_comparison.csv',index=False)
    print(comparison.to_string(index=False),flush=True)
    print('Primary',p,diag['active_bounds'],extrema(p),flush=True)
    sensitivity=[]
    for floor,cap in [(.5,20),(2.,20),(1.,10),(1.,50)]:
        pp,tt,dd=fit(z,starts=80,floor=floor,cap=cap,warm=[t])
        sensitivity.append({'floor_cm':floor,'alpha_cap':cap,'loglik':dd['best_loglik'],'active':dd['active_bounds'],'extrema':extrema(pp),'parameters':[v.tolist() for v in pp]})
    print('Sensitivity complete; bootstrap 200 x 20 random starts plus primary warm start',flush=True)
    boots=[]; failures=[]; diagnostics=[]
    for b in range(200):
        xb=rng.choice(x,n,replace=True)
        try:
            pp,tt,dd=fit((xb-center)/unit,starts=20,warm=[t])
            mm,ss,mu,sigma=moments(pp); ex=extrema(pp,4097)
            modes=[e['position'] for e in ex if e['type']=='mode']
            row={'replicate':b,'mode_count':len(modes),'mixture_mean':mu,'mixture_sd':sigma,'loglik':dd['best_loglik'],'active':';'.join(dd['active_bounds']), 'converged_starts':dd['converged'],'attempted_starts':dd['attempted']}
            for j in range(2):
                for key,vals in [('weight',pp[0]),('location',pp[1]),('scale',pp[2]),('alpha',pp[3]),('mean',mm),('sd',ss)]: row[f'c{j+1}_{key}']=vals[j]
            row['lower_mode_if_two']=modes[0] if len(modes)==2 else np.nan
            row['upper_mode_if_two']=modes[1] if len(modes)==2 else np.nan
            boots.append(row)
        except Exception as e: failures.append({'replicate':b,'error':str(e)})
        if (b+1)%20==0: print(f'Bootstrap {b+1}/200; successful {len(boots)}',flush=True)
    boot=pd.DataFrame(boots); boot.to_csv(OUT/'heights_bootstrap.csv',index=False)
    numeric=[c for c in boot if c.startswith('c') and c!='converged_starts']+['mixture_mean','mixture_sd','lower_mode_if_two','upper_mode_if_two']
    intervals=boot[numeric].quantile([.025,.5,.975]).T
    intervals.columns=['p2.5','median','p97.5']; intervals.to_csv(OUT/'heights_bootstrap_intervals.csv')
    w,l,s,a=p; mm,ss,mu,sigma=moments(p)
    components=pd.DataFrame({'component':[1,2],'weight':w,'location_cm':l,'scale_cm':s,'alpha':a,'mean_cm':mm,'sd_cm':ss})
    components.to_csv(OUT/'heights_components.csv',index=False)
    lp=np.log(w)+skewnorm.logpdf(x[:,None],a,loc=l,scale=s)
    post=np.exp(lp-logsumexp(lp,axis=1)[:,None])
    cleaned=pd.DataFrame({'source_row':np.flatnonzero(keep)+2,'height_cm':x,'posterior_component_1':post[:,0],'posterior_component_2':post[:,1]})
    cleaned.to_csv(OUT/'heights_cleaned.csv',index=False,float_format='%.15g')
    qs=[quantile(q,p) for q in [.1,.5,.9]]
    qlo,qmed,qhi=qs
    counts=[int(np.sum(x<qlo)),int(np.sum((x>=qlo)&(x<=qhi))),int(np.sum(x>qhi))]
    probs=[float(cdf(qlo,p)),float(cdf(qhi,p)-cdf(qlo,p)),float(1-cdf(qhi,p))]
    probtable=pd.DataFrame({'region':['X < q10','q10 <= X <= q90','X > q90'],'count':counts,'empirical_probability':np.array(counts)/n,'model_probability':probs})
    probtable['absolute_difference']=abs(probtable.empirical_probability-probtable.model_probability)
    probtable['relative_error_percent']=100*probtable.absolute_difference/probtable.model_probability.replace(0,np.nan)
    probtable.to_csv(OUT/'heights_probabilities.csv',index=False)
    stats={'n_original':len(values),'n_retained':n,'invalid_missing':int((~keep).sum()),'mean_cm':x.mean(),'variance_cm2':x.var(ddof=1),'sd_cm':x.std(ddof=1),'median_cm':np.median(x),'min_cm':x.min(),'max_cm':x.max(),'percentiles_cm':dict(zip(['1','5','10','25','50','75','90','95','99'],np.percentile(x,[1,5,10,25,50,75,90,95,99]))),'unique':len(np.unique(x)),'integer_observations':int(np.sum(x==np.round(x))), 'lag1_correlation':float(np.corrcoef(x[:-1],x[1:])[0,1]),'order_spearman':float(spearmanr(np.arange(n),x).statistic)}
    modes=extrema(p); fine=extrema(p,32769)
    ks=float(kstest(x,lambda v:cdf(v,p)).statistic); cvm=float(cramervonmises(x,lambda v:cdf(v,p)).statistic)
    results={'seed':SEED,'sha256_input':hashlib.sha256(raw).hexdigest(),'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__},'sample':stats,'fit_diagnostics':diag,'alternative_diagnostics':{'skew_normal':sd,'two_normals':nd},'sensitivity':sensitivity,'parameters':[v.tolist() for v in p],'mixture_mean':mu,'mixture_sd':sigma,'extrema':modes,'extrema_fine':fine,'domain':domain(p),'quantiles_10_50_90':qs,'KS':ks,'CvM':cvm,'probability_below_zero':float(cdf(0,p)),'bootstrap_requested':200,'bootstrap_successful':len(boot),'bootstrap_failures':failures,'bootstrap_mode_counts':{str(k):int(v) for k,v in boot.mode_count.value_counts().items()},'bootstrap_active_fraction':float((boot.active!='').mean()),'bootstrap_failed_starts':int((boot.attempted_starts-boot.converged_starts).sum())}
    (OUT/'heights_results.json').write_text(json.dumps(results,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),encoding='utf-8')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160})
    xx=np.linspace(x.min()-10,x.max()+10,2000)
    fig,ax=plt.subplots(figsize=(8,4.4))
    ax.hist(x,bins='fd',density=True,color='#cbd5e1',edgecolor='white',label='Observed (Freedman-Diaconis)')
    ax.plot(xx,density(xx,p),color='#0f172a',lw=2,label='Total mixture')
    for j in range(2): ax.plot(xx,w[j]*skewnorm.pdf(xx,a[j],loc=l[j],scale=s[j]),lw=1.8,label=f'Weighted component {j+1}')
    ax.set(xlabel='Height (cm)',ylabel='Density (1/cm)'); ax.legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'heights_density.png');plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(11,3.6),sharey=True)
    for ax,bins in zip(axes,[6,10,20]):
        ax.hist(x,bins=bins,density=True,color='#cbd5e1',edgecolor='white');ax.plot(xx,density(xx,p),color='#0f172a');ax.set(title=f'{bins} equal-width bins',xlabel='Height (cm)')
    axes[0].set_ylabel('Density (1/cm)');fig.tight_layout();fig.savefig(OUT/'heights_bins.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.3));sx=np.sort(x)
    ax.step(np.r_[xx[0],sx,xx[-1]],np.r_[0,np.arange(1,n+1)/n,1],where='post',label='Empirical CDF')
    ax.plot(xx,cdf(xx,p),label='Fitted mixture CDF');ax.set(xlabel='Height (cm)',ylabel='Cumulative probability');ax.legend();fig.tight_layout();fig.savefig(OUT/'heights_cdf.png');plt.close(fig)
    theoretical=np.array([quantile(v,p) for v in (np.arange(1,n+1)-.5)/n])
    fig,ax=plt.subplots(figsize=(6,4.5));ax.scatter(theoretical,sx,s=15);ax.plot([145,195],[145,195],color='gray',ls='--');ax.set(xlabel='Fitted mixture quantiles (cm)',ylabel='Observed quantiles (cm)');fig.tight_layout();fig.savefig(OUT/'heights_qq.png');plt.close(fig)
    print('Analysis complete. Results saved.',flush=True)
