import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader


class ListingsItem(scrapy.Item):
    rental_id = Field()
    anyrooms = Field()
    anyrooms_description = Field()
    bedrooms = Field()
    bedrooms_description = Field()
    baths_short_description = Field()
    baths_description = Field()
    listed_price = Field()
    title_with_unit = Field()
    large_image_uri = Field()
    unit_type = Field()
    url = Field()
    building_id = Field()
    building_url = Field()
    building_type = Field()
    building_residential_unit_count = Field()
    building_year_built = Field()
    pretty_address = Field()
    unit = Field()
    area_id = Field()
    area_name = Field()
    contact_id = Field()
    contact_name = Field()
    contact_phone = Field()
    business_name = Field()


class ListingsLoader(ItemLoader):
    """ItemLoader for a ListingsItem object"""