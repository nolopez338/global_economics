import test from 'node:test';
import assert from 'node:assert/strict';
import {MagneticRotation} from '../assets/js/pvc-rotation.mjs';
const rad=d=>d*Math.PI/180,deg=r=>r*180/Math.PI;
const near=(a,b,t=1e-8)=>assert(Math.abs(a-b)<t,`${a} != ${b}`);
const move=(s,d)=>deg(s.update(rad(d)));
const targets=[0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330,360];

test('every target captures from both directions on negative and multiple turns',()=>{
  for(const turn of [-3,-1,0,1,4])for(const target of targets)for(const direction of [-1,1]){
    const s=new MagneticRotation(),angle=target+turn*360;
    move(s,angle+direction*9);
    near(move(s,angle+direction*3),angle);
    near(move(s,angle-direction*4.99),angle);
    assert.notEqual(move(s,angle-direction*5.01),angle);
    near(move(s,angle-direction*9),angle-direction*9);
  }
});
test('hysteresis holds against jitter, releases and re-arms only outside 5 degrees',()=>{
  const s=new MagneticRotation();
  move(s,20);near(move(s,28),30);
  for(const angle of [26,32,25,35,27,33])near(move(s,angle),30);
  assert.notEqual(move(s,35.1),30);
  near(move(s,39),39);
  near(move(s,33),30);
  near(move(s,25),30);
  near(move(s,21),21);
});
test('release is continuous and reaches exact arbitrary angles beyond the easing band',()=>{
  for(const direction of [-1,1]){
    const s=new MagneticRotation();move(s,20);move(s,30);
    near(move(s,30+direction*5),30);
    near(move(s,30+direction*5.00001),30,1e-7);
    let previous=30;
    for(let d=5.01;d<=8;d+=.01){
      const angle=move(s,30+direction*d);
      assert((angle-previous)*direction>=-1e-8);previous=angle;
    }
    near(move(s,30+direction*8),30+direction*8);
    near(move(s,30+direction*9.12345),30+direction*9.12345);
  }
});
test('reversing after release does not re-capture outside the capture zone',()=>{
  const s=new MagneticRotation();move(s,20);move(s,30);move(s,35.1);
  assert(move(s,34.9)>30);assert.equal(s.held,null);
  move(s,34);assert.equal(s.held,null);
  near(move(s,33),30);assert.notEqual(s.held,null);
});
test('unbounded axis displacement never wraps even after large pointer samples',()=>{
  const s=new MagneticRotation();
  for(const angle of [720+9.123,-720-9.123,1080+17.2,-1080-17.2])near(move(s,angle),angle);
});
test('wrapped in-plane pointer input unwraps across both seams for multiple revolutions',()=>{
  for(const direction of [-1,1]){
    const s=new MagneticRotation({wrapped:true});
    for(let i=0;i<=1100;i++){
      const angle=i*direction,principal=((angle+180)%360+360)%360-180;
      const output=move(s,principal);near(deg(s.raw),angle);
      assert(Math.abs(output-angle)<=5.1,'Unexpected jump at '+angle);
      if(i%360===0)near(output,angle);
    }
  }
});
test('0 and 360 share one target and a fresh drag has fresh hysteresis',()=>{
  const s=new MagneticRotation();move(s,350);near(move(s,358),360);
  for(const a of [359,360,361,355,365])near(move(s,a),360);
  near(move(s,369.5),369.5);
  const fresh=new MagneticRotation();near(move(fresh,-3),0);near(move(fresh,5),0);
});
