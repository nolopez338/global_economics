import {orientedBox} from './pvc-bounds.mjs';
self.onmessage=({data})=>{try{self.postMessage({box:orientedBox(data.points,data.seeds)});}catch(error){self.postMessage({error:error.message});}};
