import hashlib; from typing import List,Tuple; EMBED_DIM=8
def _vec(t:str)->List[float]:
    h=hashlib.sha256(t.encode()).digest(); vals=[h[i]/255.0 for i in range(EMBED_DIM)]; s=sum(vals) or 1.0; return [v/s for v in vals]
def chunk_text(text:str,max_chars:int=300)->List[str]:
    chunks=[]; cur=""; 
    for line in text.strip().replace("\r","\n").split("\n"):
        if len(cur)+len(line)+1>max_chars and cur: chunks.append(cur.strip()); cur=""
        cur+=(" " if cur else "")+line.strip()
    if cur: chunks.append(cur.strip()); 
    return chunks[:20] or [text[:max_chars]]
def embed_chunks(chunks:List[str])->List[List[float]]: return [_vec(c) for c in chunks]
def nearest_k(q:str,items:List[Tuple[str,List[float]]],k:int=3): 
    v=_vec(q); dot=lambda a,b: sum(x*y for x,y in zip(a,b)); s=[(t,dot(v,x)) for t,x in items]; s.sort(key=lambda x:x[1],reverse=True); return s[:k]
