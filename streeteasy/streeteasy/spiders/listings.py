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
            "variables": {"ids": listing_ids[:2]},
            # "variables": {"ids": listing_ids},
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
        if data.get("data") is None:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        for item in data["data"]["rentals"]:
            l = ListingsLoader(ListingsItem())
            l.add_value('rental_id', item["id"])
            l.add_value('anyrooms', item["anyrooms"])
            l.add_value('anyrooms_description', item["anyrooms_description"])
            l.add_value('bedrooms', item["bedrooms"])
            l.add_value('bedrooms_description', item["bedrooms_description"])
            l.add_value('bathrooms', item["bathrooms"])
            l.add_value('baths_short_description', item["baths_short_description"])
            l.add_value('listed_price', item["listed_price"])
            l.add_value('title_with_unit', item["title_with_unit"])
            l.add_value('large_image_uri', item["large_image_uri"])
            l.add_value('unit_type', item["unit_type"])
            l.add_value('url', item["url"])

            building = item["building"]
            l.add_value('building_id', building["id"])
            l.add_value('building_url', building["url"])
            l.add_value('building_type', building["building_type"])
            l.add_value('building_residential_unit_count', building["residential_unit_count"])
            l.add_value('building_year_built', building["year_built"])

            address = item["address"]
            l.add_value('pretty_address', address["pretty_address"])
            l.add_value('unit', address["unit"])

            area = item["area"]
            l.add_value('area_id', area["id"])
            l.add_value('area_name', area["name"])

            contact = item["contacts"][0]  # actually a list
            l.add_value('contact_id', contact["id"])
            l.add_value('contact_name', contact["name"])
            l.add_value('contact_phone', contact["phone"])
            l.add_value('contact_email', contact["email"])
            l.add_value('business_name', contact["business_name"])
            # business ID or URL ?
            yield l.load_item()
