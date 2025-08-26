import os,re,requests,trafilatura; from typing import Tuple
def _read_local(p): 
    try: return open(p,"r",encoding="utf-8",errors="ignore").read()
    except Exception: return "Stub content (binary/unreadable)."
def fetch_web(url)->Tuple[str,str]:
    if url.startswith("file://"): 
        p=url[len("file://"):]; c=_read_local(p); t=trafilatura.extract(c) or c[:4000]; return (t or "No text extracted.","en")
    r=requests.get(url,timeout=15); r.raise_for_status(); e=trafilatura.extract(r.text) or r.text; return (e[:20000],"en")
def fetch_youtube_stub(url)->str:
    v="/app/samples/youtube_sample.vtt"
    if os.path.exists(v):
        t=_read_local(v); out=[]; 
        for line in t.splitlines():
            if re.match(r"^\\d{2}:\\d{2}:",line): continue
            if line.strip() and not line.startswith("WEBVTT"): out.append(line.strip())
        return " ".join(out)[:20000]
    return "Sample YouTube transcript text with timestamps [00:00-00:05]."
def fetch_file_stub(path,stype)->str: return f"Stub extracted text from {stype.upper()} file: {os.path.basename(path)}."
def ingest_by_type(source_type,url_or_path)->Tuple[str,str]:
    st=source_type.lower()
    if st=="web": return fetch_web(url_or_path)
    if st=="youtube": return fetch_youtube_stub(url_or_path),"en"
    if st in {"pdf","docx","pptx","audio","instagram"}: return fetch_file_stub(url_or_path or "",st),"en"
    return "Unsupported source type.","en"
