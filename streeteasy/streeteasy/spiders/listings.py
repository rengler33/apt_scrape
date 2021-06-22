from pathlib import Path
import json

import chompjs
import scrapy

from streeteasy.items import ListingsItem, ListingsLoader


class ListingsSpider(scrapy.Spider):
    """ListingsSpiders collects listing IDs for active rentals in an
    area and queries the internal GraphQL API for information about
    those IDs. `area` is a required CLI argument e.g. -a area=brooklyn.
    """

    name = "listings"

    def start_requests(self):
        if getattr(self, "area", None) is None:
            self.logger.error("Need to supply 'area' argument.")
            return
        url = f"https://streeteasy.com/for-rent/{self.area}?view=map"
        yield scrapy.Request(url=url, callback=self.get_listing_ids)

    def get_listing_ids(self, response):
        script = response.css("script:contains('dataLayer =')::text")
        obj = chompjs.parse_js_object(script.get())
        listing_ids = obj[0]["searchResultsListings"].split("|")
        yield {"ids": listing_ids}
        self.logger.info("Found %s ID's", len(listing_ids))

        headers = {
            "content-type": "application/json",
        }
        with open(Path(__file__).parent / "listings.graphql") as f:
            query = f.read()
        url = "https://api-internal.streeteasy.com/graphql"
        data_dict = {
            "operationName": "rentals",
            "variables": {"ids": listing_ids},
            "query": query,
        }

        data_raw = json.dumps(data_dict)
        yield scrapy.Request(
            url=url,
            callback=self.get_listing_details,
            method="POST",
            headers=headers,
            body=data_raw,
        )

    def get_listing_details(self, response):
        data = json.loads(response.text)
        for item in data["data"]["rentals"]:
            yield item
