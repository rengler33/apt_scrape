import json
from pathlib import Path

import httpx 

headers = {
    'Origin': 'https://streeteasy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'content-type': 'application/json',
}

with open("streeteasy/ids.jl") as f:
    ids = json.loads(f.read())["ids"]
ids = ids[0]

with open(Path(__file__).parent / "rental_query.graphql") as f:
    query = f.read()
    
data_dict = {
    "operationName":"rentals",
    "variables": {"ids": ids},
    "query": query,
}

data_raw = json.dumps(data_dict)

response = httpx.post(
    'https://api-internal.streeteasy.com/graphql', 
    headers=headers,
    content=data_raw,
    timeout=None,
)

print(response.text)

