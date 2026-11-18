import subprocess,tempfile,time,json,urllib.request,websocket,socket,threading,http.server,os
from pathlib import Path
root=Path.cwd()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),http.server.SimpleHTTPRequestHandler)
threading.Thread(target=server.serve_forever,daemon=True).start()
sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
profile=tempfile.mkdtemp(prefix='population-browser-')
chrome=subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe','--headless=new','--disable-gpu','--no-first-run','--remote-allow-origins=*',f'--remote-debugging-port={port}',f'--user-data-dir={profile}','about:blank'],creationflags=subprocess.CREATE_NO_WINDOW,stdout=open(root/'tmp/chrome-out.log','w'),stderr=open(root/'tmp/chrome-err.log','w'))
for _ in range(60):
 try:
  tabs=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=1));break
 except Exception as e: print(type(e).__name__,chrome.poll(),flush=True); time.sleep(.2)
ws=websocket.create_connection(tabs[0]['webSocketDebuggerUrl'],timeout=15)
counter=0
errors=[]
def call(method,params={}):
 global counter
 counter+=1; ident=counter;ws.send(json.dumps({'id':ident,'method':method,'params':params}))
 while True:
  result=json.loads(ws.recv())
  if result.get('method')=='Runtime.exceptionThrown':errors.append(result)
  if result.get('id')==ident:
   if 'error' in result:raise Exception(result['error'])
   return result.get('result',{})
def js(code):
 result=call('Runtime.evaluate',{'expression':code,'returnByValue':True,'awaitPromise':True})
 if 'exceptionDetails' in result:raise Exception(result['exceptionDetails'])
 return result.get('result',{}).get('value')
call('Runtime.enable');call('Page.enable')
call('Emulation.setDeviceMetricsOverride',{'width':1280,'height':1000,'deviceScaleFactor':1,'mobile':False})
call('Page.navigate',{'url':f'http://127.0.0.1:{server.server_port}/general_fundamentals/population_sample_simulation.html'})
time.sleep(1)
print(js("JSON.stringify({title:document.title,N:state.students.length,summary:$('summary').textContent})"))
print(js("$('add-one').click(); go(4); JSON.stringify({N:state.students.length,z:interval().z,mean,selected:[...selected]})"))
print('errors',errors)
ws.close();chrome.terminate();server.shutdown()

