// Drag angles are offsets about the shared world-axis pivot, in radians.
const TURN=2*Math.PI, DEG=Math.PI/180;
const TARGETS=[0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330];
const CAPTURE=3*DEG, RELEASE=5*DEG, BLEND=3*DEG, EPSILON=1e-12;

export class MagneticRotation {
  constructor({wrapped=false}={}){
    this.wrapped=wrapped;this.previous=0;this.raw=0;
    this.held=0;this.released=null;this.releaseTravel=0;
  }
  update(pointerAngle){
    // Only the camera-facing ring reports a principal angle. Ordinary axis
    // handles report an unbounded linear displacement: never unwrap those.
    let delta=pointerAngle-this.previous;
    if(this.wrapped)delta=Math.atan2(Math.sin(delta),Math.cos(delta));
    this.previous=pointerAngle;this.raw+=delta;
    if(this.released!==null)this.releaseTravel+=Math.abs(delta);
    if(this.held!==null){
      if(Math.abs(this.raw-this.held)<=RELEASE+EPSILON)return this.held;
      // Leaving the release zone re-arms this target for a later approach.
      this.released=this.held;this.held=null;
      this.releaseTravel=Math.abs(this.raw-this.released)-RELEASE;
    }
    let nearest=null,distance=Infinity;
    for(const degrees of TARGETS){
      const base=degrees*DEG,target=base+Math.round((this.raw-base)/TURN)*TURN;
      const gap=Math.abs(this.raw-target);
      if(gap<distance){nearest=target;distance=gap;}
    }
    if(distance<=CAPTURE+EPSILON){this.held=nearest;this.released=null;return nearest;}
    if(this.released!==null){
      // A short spatial easing band avoids a 5-degree jump on release. It
      // reaches the exact raw angle after 3 more degrees of pointer travel.
      // Counting travel also allows reversal without silently re-capturing
      // outside the 3-degree capture zone. Every angle remains selectable.
      const t=Math.max(0,this.releaseTravel/BLEND);
      if(t<1)return this.released+(this.raw-this.released)*t*t*(3-2*t);
      this.released=null;
    }
    return this.raw;
  }
}
