// Run with sharp available on NODE_PATH. Recreates the constrained raster edit.
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const dir = __dirname;
const stem = 'Global_Economics_cover';
const bars = [[186,254,1157],[254,321,1122],[321,388,1057],
  [388,456,972],[456,524,889],[524,593,845],[593,661,889],
  [661,730,972],[730,798,1057],[798,866,1122],[866,935,1157]];
let state = 20261113;
function random() {
  state |= 0; state = state + 0x6D2B79F5 | 0;
  let t = Math.imul(state ^ state >>> 15, 1 | state);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
  return ((t ^ t >>> 14) >>> 0) / 4294967296;
}
(async () => {
  const {data: original, info} = await sharp(path.join(dir, stem+'_artwork.png')).raw().toBuffer({resolveWithObject:true});
  const grain = await sharp(path.join(dir, stem+'_artwork_grain.png')).removeAlpha().raw().toBuffer();
  const out = Buffer.from(grain), {width:w,height:h,channels:c} = info;
  const at = (a,x,y,k=0) => a[(Math.max(0,Math.min(h-1,y))*w+Math.max(0,Math.min(w-1,x)))*c+k];
  const curveY = x => 1169 - 341.2*Math.exp(-0.5*((x-558.5)/133.4)**2);
  const nearCurve = (x,y,r=8) => Math.abs(y-curveY(x))<r;
  const modified = new Uint8Array(w*h);
  const adjustments = bars.map(([left,right,top]) => {
    const change = (random()*2-1)*0.08;
    return {left,right,top,oldHeight:1169-top,newHeight:(1169-top)*(1+change),changePercent:change*100,newTop:1169-(1169-top)*(1+change)};
  });
  // Work only in the narrow bands swept out by the old and new bar tops.
  for (const b of adjustments) {
    const lo = Math.floor(Math.min(b.top,b.newTop))-4;
    const hi = Math.ceil(Math.max(b.top,b.newTop))+6;
    for (let y=lo;y<=hi;y++) for(let x=b.left-3;x<=b.right+3;x++) modified[y*w+x]=1;
  }
  function background(x,y,k) {
    // Existing ungrained white paper, at the same height away from the graph.
    return at(original,960+(x%41),y,k);
  }
  function sample(x,y,k) {
    const y0=Math.floor(y), f=y-y0;
    return Math.round(at(grain,x,y0,k)*(1-f)+at(grain,x,y0+1,k)*f);
  }
  for(let y=800;y<1166;y++) for(let x=182;x<940;x++) {
    if(!modified[y*w+x]) continue;
    let b = adjustments.find(b=>x>=b.left && x<b.right);
    for(let k=0;k<c;k++) {
      let v = background(x,y,k);
      if(b && y>=b.newTop-4) {
        let sx=x, sy=b.top+y-b.newTop;
        // Never translate an original piece of the normal curve with a bar.
        if(y<=b.newTop+4) {
          if(nearCurve(sx,sy,20)) {
            const candidates=[b.left+10,Math.round((b.left+b.right)/2),b.right-10];
            sx=candidates.sort((a,z)=>Math.abs(curveY(z)-sy)-Math.abs(curveY(a)-sy))[0];
          }
        } else {
          // Sample established grain well inside the source bar; avoid both
          // the old top's raster ringing and the curve's pale edge halo.
          sy=Math.max(b.top+15,Math.min(1155,Math.floor(sy)+20));
          while(nearCurve(sx,sy,20) && sy<1155) sy+=1;
        }
        v=sample(sx,sy,k);
      }
      out[(y*w+x)*c+k]=v;
    }
  }
  // Reuse original side-edge profiles. Shared boundaries start at the taller
  // of their adjacent bars and retain their original x position and width.
  for(let j=0;j<=bars.length;j++) {
    const x0=j===bars.length?bars[j-1][1]:bars[j][0];
    const neighbors=[adjustments[j-1],adjustments[j]].filter(Boolean);
    const oldTop=Math.min(...neighbors.map(b=>b.top));
    const newTop=Math.min(...neighbors.map(b=>b.newTop));
    for(let y=800;y<1166;y++) for(let x=x0-2;x<=x0+2;x++) {
      if(!modified[y*w+x]) continue;
      for(let k=0;k<c;k++) {
        let v=background(x,y,k);
        if(y>=newTop-3) {
          let sy=oldTop+y-newTop;
          if(y>newTop+6) {
            const both=neighbors.length===2 && neighbors.every(b=>y>b.newTop+5);
            sy=both?1150:oldTop+10;
            while(nearCurve(x,sy,10)) sy+=12;
          }
          v=sample(x,sy,k);
        }
        out[(y*w+x)*c+k]=v;
      }
    }
  }
  // Locate the existing curve from clean columns, interpolating through bar
  // intersections. Copy its stroke pixels, never the obsolete bar-top pixels
  // or the old fill/background surrounding the stroke.
  const centers=[];
  for(let x=182;x<940;x++) {
    if(bars.some(b=>Math.abs(x-b[0])<5 || Math.abs(x-b[1])<5)) continue;
    if(bars.some(b=>Math.abs(curveY(x)-b[2])<12)) continue;
    const ys=[];
    for(let y=Math.floor(curveY(x))-7;y<=Math.ceil(curveY(x))+7;y++) {
      if(y>=1165) continue;
      if(at(original,x,y)<80) ys.push(y);
    }
    if(ys.length>=2) centers.push([x,(ys[0]+ys[ys.length-1])/2]);
  }
  function centerAt(x) {
    let i=centers.findIndex(p=>p[0]>=x);
    if(i<=0) {
      const p=i===0?centers[0]:centers[centers.length-1];
      return curveY(x)+p[1]-curveY(p[0]);
    }
    const [a,b]=[centers[i-1],centers[i]];
    const ra=a[1]-curveY(a[0]), rb=b[1]-curveY(b[0]);
    return curveY(x)+ra+(rb-ra)*(x-a[0])/(b[0]-a[0]);
  }
  let curvePixels=0,changed=0,outside=0;
  for(let y=800;y<1166;y++) for(let x=182;x<940;x++) {
    const slope=(curveY(x+1)-curveY(x-1))/2;
    const radius=2.1*Math.sqrt(1+slope*slope)+0.3;
    if(Math.abs(y-centerAt(x))<=radius && at(original,x,y)<230) {
      for(let k=0;k<c;k++) out[(y*w+x)*c+k]=grain[(y*w+x)*c+k];
      curvePixels++;
    }
  }
  for(let p=0;p<w*h;p++) {
    let different=false;
    for(let k=0;k<c;k++) different ||= out[p*c+k]!==grain[p*c+k];
    if(different) { changed++; if(!modified[p]) outside++; }
  }
  if(outside) throw new Error('Changes escaped the bar-height masks');
  if(adjustments.some(b=>Math.abs(b.changePercent)>8 || b.newHeight<=0)) throw new Error('Invalid height');
  await sharp(out,{raw:info}).png().toFile(path.join(dir,stem+'_artwork_irregular.png'));
  const report={seed:20261113,dimensions:[w,h],baseline:1169,changedPixels:changed,changesOutsideHeightMasks:outside,protectedCurveStrokePixels:curvePixels,bars:adjustments};
  fs.writeFileSync(path.join(dir,stem+'_histogram_verification.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
})();
