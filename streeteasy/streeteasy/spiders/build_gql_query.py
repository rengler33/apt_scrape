import json
from pathlib import Path

import httpx 

headers = {
    'Origin': 'https://streeteasy.com',  # seems to be optional
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'content-type': 'application/json',
}

with open("streeteasy/ids.jl") as f:
    ids = json.loads(f.read())["ids"]
ids = ids[0]  # take only first one so as not to spam the server

# introspection seems not allowed
# with open(Path(__file__).parent / "introspection.graphql") as f:
#     query = f.read()

with open(Path(__file__).parent / "rental_query.graphql") as f:
    query = f.read()
    
data_dict = {
    # "operationName":"rentals",  # seems to be optional
    "variables": {"ids": ids},
    "query": query,
}

data_raw = json.dumps(data_dict)

response = httpx.post(
    'https://api-internal.streeteasy.com/graphql', 
    headers=headers,
    content=data_raw,
    timeout=10,  # longer timeout needed if sending lots of IDs
)

data = json.loads(response.text)

print(json.dumps(data, indent=2))

