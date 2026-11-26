/* Shared numerical model for the C3 presentation and its independent checks. */
((root) => {
  'use strict';
  // Convergent integral series for Φ. Absolute error below 3e-14 over the
  // lesson's [-4,4] domain, including the small tail at z = 3.291.
  function cdf(x) {
    if(x>8) return 1; if(x< -8) return 0;
    let sum=x,term=x;
    for(let k=1;k<180;k++){term*=x*x/(2*k+1);sum+=term;if(Math.abs(term)<1e-17*Math.abs(sum))break;}
    return .5+sum*Math.exp(-x*x/2)/Math.sqrt(2*Math.PI);
  }
  function invCdf(prob) {
    if(!(prob>0&&prob<1)) throw new RangeError('Normal probability must be between 0 and 1.');
    let lo=-8,hi=8;
    for(let k=0;k<64;k++){const mid=(lo+hi)/2;if(cdf(mid)<prob)lo=mid;else hi=mid;}
    return (lo+hi)/2;
  }
  function model(n,z){
    if(!Number.isInteger(n)||n<1)throw new RangeError('Sample size must be a positive integer.');
    if(!Number.isFinite(z)||z<0)throw new RangeError('Critical value must be finite and nonnegative.');
    const se=30/Math.sqrt(n),moe=z*se;
    return {n,z,se,moe,l:84-moe,u:84+moe,coverage:100*(2*cdf(z)-1)};
  }
  const api=Object.freeze({model,cdf,invCdf});
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.G11C3Math=api;
})(globalThis);
