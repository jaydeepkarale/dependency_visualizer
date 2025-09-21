from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import yaml
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile):
    content = (await file.read()).decode("utf-8")
    data = yaml.safe_load(content)

    component = data.get("component", os.path.splitext(file.filename)[0])
    nodes = {component: {"id": component, "label": component, "info": "Main Component"}}
    edges = []

    # Upstreams
    for system, meta in (data.get("upstream") or {}).items():
        nodes[system] = {"id": system, "label": system, "info": meta.get("info", "")}
        edges.append({"from": system, "to": component})

    # Downstreams
    for system, meta in (data.get("downstream") or {}).items():
        nodes[system] = {"id": system, "label": system, "info": meta.get("info", "")}
        edges.append({"from": component, "to": system})

    return {
        "component": component,
        "nodes": list(nodes.values()),
        "edges": edges,
    }
