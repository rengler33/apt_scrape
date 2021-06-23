import json
from pathlib import Path

import httpx 


def introspection_query():
    # introspection seems not allowed
    with open(Path(__file__).parent / "introspection.graphql") as f:
        query = f.read()
    return query


def rentals_query():
    with open("streeteasy/ids.jl") as f:
        ids = json.loads(f.read())["ids"]
    ids = ids[0]  # take only first one so as not to spam the server

    with open(Path(__file__).parent / "rental.graphql") as f:
        query = f.read()
    
    return ids, query


def buildings_query():
    ids = ["422096"]  # example building

    with open(Path(__file__).parent / "building.graphql") as f:
        query = f.read()
    
    return ids, query



def listings_query():
    with open("streeteasy/ids.jl") as f:
        ids = json.loads(f.read())["ids"]
    ids = ids[0]  # take only first one so as not to spam the server

    with open(Path(__file__).parent.parent/ "spiders" / "listings.graphql") as f:
        query = f.read()
    
    return ids, query

def main():
    headers = {
        # 'Origin': 'https://streeteasy.com',  # optional here, seems to break the spider
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'content-type': 'application/json',
    }

    # ids, query = buildings_query()
    ids, query = rentals_query()
    # ids, query = listings_query()

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

    return data


if __name__ == "__main__":
    data = main()
    print(json.dumps(data, indent=2))

