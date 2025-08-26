from fastapi.testclient import TestClient; from app import app; from db import init_db; from tasks import run_pipeline; import os
c=TestClient(app)
def test_pipeline():
    init_db()
    web=c.post("/v1/sources/json",json={"source_type":"web","url_or_path":"file:///app/samples/sample.html"}).json()["id"]
    pdf=c.post("/v1/sources/json",json={"source_type":"pdf","url_or_path":"/app/samples/sample.pdf"}).json()["id"]
    yt=c.post("/v1/sources/json",json={"source_type":"youtube","url_or_path":"https://youtube.com/watch?v=abc"}).json()["id"]
    job=c.post("/v1/pipelines/run",json={"source_ids":[web,pdf,yt],"export_options":{}}).json()["job_id"]
    run_pipeline(job,[web,pdf,yt],{})
    j=c.get(f"/v1/jobs/{job}").json(); assert j["status"]=="completed"; ex=j["result"]["exports"]
    assert all(os.path.exists(ex[k]) for k in ["pptx","pdf","html","md","json"])
