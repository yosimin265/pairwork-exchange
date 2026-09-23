#!/usr/bin/env python3
"""PairWork: loopback-only, two-person hackathon demo. Python 3.10+."""
import hashlib, json, os, secrets, sqlite3, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
DATA=Path(os.environ.get('PAIRWORK_DATA',str(ROOT/'.pairwork')))
DATA.mkdir(exist_ok=True)
DB=DATA/'demo.sqlite3'
SESSIONS={}; DEVICES={}; TOKENS={}

def seed():
 return {'pairs':[{'id':'a','name':'Kai + Codex','specialty':'Python / Code review','balance':300,'completed':0}, {'id':'b','name':'Mio + Claude Code','specialty':'Translation / Documentation','balance':300,'completed':0}], 'jobs':[{'id':'job-001','creator':'a','worker':None,'title':'READMEを英語に翻訳','description':'# PairWork\n人間とAIのチームで仕事を交換します。得意な仕事でポイントを獲得し、苦手な仕事を依頼できます。','category':'Translation','points':50,'status':'open','result':'','hash':None,'receipt':None}], 'ledger':[], 'events':['デモを開始しました。各チーム300pt。']}

def connection():
 c=sqlite3.connect(DB,timeout=10);c.execute('CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, data TEXT NOT NULL)')
 c.execute('INSERT OR IGNORE INTO state VALUES (1,?)',(json.dumps(seed(),ensure_ascii=False),));c.commit();return c

def read_state():
 with connection() as c:return json.loads(c.execute('SELECT data FROM state WHERE id=1').fetchone()[0])

def apply(s,who,action,args):
 pairs={p['id']:p for p in s['pairs']}
 if who not in pairs:raise ValueError('ログインしてください')
 if action=='create_job':
  title=str(args.get('title','')).strip(); desc=str(args.get('description','')).strip();points=args.get('points',50)
  if not title or len(title)>120 or not desc or len(desc)>12000:raise ValueError('件名と依頼内容を入力してください')
  if type(points)!=int or not 1<=points<=300:raise ValueError('ポイントは1〜300の整数です')
  reserved=sum(j['points'] for j in s['jobs'] if j['creator']==who and j['status'] not in ('completed','cancelled'))
  if pairs[who]['balance']-reserved<points:raise ValueError('予約済みポイントを除いた残高が不足しています')
  j={'id':'job-'+secrets.token_hex(4),'creator':who,'worker':None,'title':title,'description':desc,'category':str(args.get('category','Code review'))[:40],'points':points,'status':'open','result':'','hash':None,'receipt':None};s['jobs'].append(j)
 else:
  j=next((j for j in s['jobs'] if j['id']==args.get('job_id')),None)
  if not j:raise ValueError('仕事が見つかりません')
  if action=='accept_job':
   if j['creator']==who or j['status']!='open':raise ValueError('この仕事は受注できません')
   j.update(worker=who,status='accepted')
  elif action=='submit_job':
   result=str(args.get('result','')).strip()
   if j['worker']!=who or j['status'] not in ('accepted','revision_requested'):raise ValueError('受注者だけが納品できます')
   if not result or len(result)>20000:raise ValueError('成果物は1〜20000文字です')
   j.update(result=result,status='submitted')
  elif action=='reject_result':
   if j['creator']!=who or j['status']!='submitted':raise ValueError('発注者だけが修正依頼できます')
   j['status']='revision_requested'
  elif action=='approve_result':
   if j['creator']!=who or j['status']!='submitted':raise ValueError('未承認の納品を発注者が承認してください')
   payer=pairs[who];payee=pairs[j['worker']]
   if payer['balance']<j['points']:raise ValueError('残高不足')
   payer['balance']-=j['points'];payee['balance']+=j['points'];payee['completed']+=1
   j['status']='completed';j['completed_at']=int(time.time())
   record={k:j[k] for k in ('id','creator','worker','points','completed_at')}
   record['result_hash']=hashlib.sha256(j['result'].encode()).hexdigest()
   j['proof']=record;j['hash']=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   s['ledger'].extend([{'job_id':j['id'],'pair':who,'amount':-j['points']},{'job_id':j['id'],'pair':j['worker'],'amount':j['points']}])
  elif action=='cancel_job':
   if j['creator']!=who or j['status']!='open':raise ValueError('募集前の仕事のみ取り消せます')
   j['status']='cancelled'
  else:raise ValueError('不明な操作です')
 s['events'].insert(0, pairs[who]['name']+' / '+action+' / '+j['title'])
 s['events']=s['events'][:30]
 return j

def mutate(who,action,args):
 c=connection()
 try:
  c.execute('BEGIN IMMEDIATE');s=json.loads(c.execute('SELECT data FROM state WHERE id=1').fetchone()[0]);j=apply(s,who,action,args)
  c.execute('UPDATE state SET data=? WHERE id=1',(json.dumps(s,ensure_ascii=False),));c.commit();return {'job':j,'state':s}
 except: c.rollback();raise
 finally:c.close()

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,code,data,cookie=None):
  blob=json.dumps(data,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(blob)))
  if cookie:self.send_header('Set-Cookie',cookie)
  self.end_headers();self.wfile.write(blob)
 def who(self):
  auth=self.headers.get('Authorization','')
  if auth.startswith('Bearer '):
   token=TOKENS.get(auth[7:]);return token['pair'] if token and token['expires']>time.time() else None
  c=SimpleCookie();c.load(self.headers.get('Cookie',''));t=c.get('pairwork');session=SESSIONS.get(t.value) if t else None
  return session['pair'] if session and session['expires']>time.time() else None
 def valid_host(self):return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')
 def do_GET(self):
  if not self.valid_host():return self.send(403,{'error':'Loopback only'})
  path=urlparse(self.path).path
  if path=='/api/state':return self.send(200,{'state':read_state(),'pair':self.who(),'mode':'server'})
  if path=='/api/profile':return self.send(200,{'pair':self.who()})
  files={'/':'index.html','/index.html':'index.html'}
  if path not in files:return self.send(404,{'error':'Not found'})
  blob=(ROOT/files[path]).read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(blob)));self.end_headers();self.wfile.write(blob)
 def do_POST(self):
  if not self.valid_host():return self.send(403,{'error':'Loopback only'})
  origin=self.headers.get('Origin')
  if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):return self.send(403,{'error':'Invalid origin'})
  try:
   if not self.headers.get('Content-Type','').startswith('application/json'):raise ValueError('JSON required')
   n=int(self.headers.get('Content-Length',0))
   if not 0<n<=30000:raise ValueError('Invalid request size')
   a=json.loads(self.rfile.read(n));path=urlparse(self.path).path
   if path=='/api/login':
    if a.get('pair') not in ('a','b'):raise ValueError('Invalid demo pair')
    token=secrets.token_urlsafe(32);SESSIONS[token]={'pair':a['pair'],'expires':time.time()+3600*8}
    return self.send(200,{'pair':a['pair']},f'pairwork={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800')
   if path=='/api/device/start':
    code=secrets.token_urlsafe(12);DEVICES[code]={'expires':time.time()+300,'pair':None}
    return self.send(200,{'code':code,'url':f'http://127.0.0.1:{self.server.server_port}/?connect={code}'})
   if path in ('/api/device/approve','/api/device/poll'):
    d=DEVICES.get(a.get('code'))
    if not d or d['expires']<time.time():raise ValueError('接続リンクの有効期限が切れました')
    if path.endswith('approve'):
     who=self.who()
     if not who:raise ValueError('先にデモログインしてください')
     d['pair']=who;return self.send(200,{'approved':True})
    if not d['pair']:return self.send(200,{'pending':True})
    token=secrets.token_urlsafe(32);TOKENS[token]={'pair':d['pair'],'expires':time.time()+28800};del DEVICES[a['code']]
    return self.send(200,{'token':token,'pair':d['pair']})
   who=self.who()
   if not who:return self.send(401,{'error':'ログインが必要です'})
   if path!='/api/action':return self.send(404,{'error':'Not found'})
   return self.send(200,mutate(who,a.get('action'),a.get('args',{})))
  except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:return self.send(400,{'error':str(e)})
  except Exception:return self.send(500,{'error':'Server error'})
if __name__=='__main__':
 port=int(os.environ.get('PORT','8765'));print(f'PairWork demo: http://127.0.0.1:{port}',flush=True)
 ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
