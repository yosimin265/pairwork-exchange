#!/usr/bin/env python3
"""Record a completion hash using a signed Memo on Solana DEVNET only.
No SOL purchase or mainnet support. Requires PyNaCl. Key is demo-only.
"""
import argparse,base64,json,os,time,urllib.request
from pathlib import Path
from nacl.signing import SigningKey
ALPH='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58(b):
 n=int.from_bytes(b,'big');s=''
 while n:n,r=divmod(n,58);s=ALPH[r]+s
 return '1'*(len(b)-len(b.lstrip(b'\0')))+s
def un58(s):
 n=0
 for ch in s:n=n*58+ALPH.index(ch)
 return b'\0'*(len(s)-len(s.lstrip('1')))+(n.to_bytes((n.bit_length()+7)//8,'big') if n else b'')
def vec(n):
 out=bytearray()
 while n>=128:out.append((n&127)|128);n>>=7
 out.append(n);return bytes(out)
def rpc(method,params):
 req=urllib.request.Request('https://api.devnet.solana.com',json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode(),{'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=25) as r:x=json.load(r)
 if 'error' in x:raise RuntimeError(str(x['error']))
 return x['result']
def main():
 p=argparse.ArgumentParser();p.add_argument('--hash',required=True);p.add_argument('--out',default='docs/devnet-receipt.json');a=p.parse_args()
 if len(a.hash)!=64 or any(c not in '0123456789abcdef' for c in a.hash):raise SystemExit('Expected lowercase SHA-256 hex')
 d=Path(__file__).resolve().parent/'.pairwork';d.mkdir(exist_ok=True);key=d/'devnet-key.bin'
 if not key.exists():
  fd=os.open(key,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  with os.fdopen(fd,'wb') as f:f.write(bytes(SigningKey.generate()))
 sk=SigningKey(key.read_bytes());pub=bytes(sk.verify_key);address=b58(pub)
 print('Devnet fee payer:',address,flush=True)
 if rpc('getBalance',[address])['value']<10000:
  print('Requesting free devnet test SOL...',flush=True);rpc('requestAirdrop',[address,100000000])
  for _ in range(12):
   if rpc('getBalance',[address])['value']>=10000:break
   time.sleep(2)
 block=rpc('getLatestBlockhash',[{'commitment':'confirmed'}])['value']['blockhash']
 memo=('PairWork:v1:'+a.hash).encode();program=un58('MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr')
 msg=bytes([1,0,1])+vec(2)+pub+program+un58(block)+vec(1)+bytes([1])+vec(1)+bytes([0])+vec(len(memo))+memo
 tx=vec(1)+sk.sign(msg).signature+msg
 sig=rpc('sendTransaction',[base64.b64encode(tx).decode(),{'encoding':'base64','preflightCommitment':'confirmed'}])
 receipt={'cluster':'devnet','completion_hash':a.hash,'fee_payer':address,'signature':sig,'status':'submitted','explorer':'https://explorer.solana.com/tx/'+sig+'?cluster=devnet'}
 for _ in range(20):
  r=rpc('getSignatureStatuses',[[sig],{'searchTransactionHistory':True}])['value'][0]
  if r and r.get('err'):raise RuntimeError(str(r['err']))
  if r and r.get('confirmationStatus') in ('confirmed','finalized'):receipt['status']=r['confirmationStatus'];receipt['slot']=r['slot'];break
  time.sleep(2)
 Path(a.out).parent.mkdir(exist_ok=True,parents=True);Path(a.out).write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
