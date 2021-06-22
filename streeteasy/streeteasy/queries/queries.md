# Queries
Queries of https://api-internal.streeteasy.com/graphql

With GraphQL, each field name needs to be known in order to retrieve it. StreetEasy has disabled introspection of the API so it's not possible to see a full list of fields. One unfortunate example of this is the fact that I've only found list price available for retrieval - if the API makes available the "net-effective price" then I haven't been able to guess its name.



It appears that `contact` is not queryable at the "QueryRoot" so it remains part of the rentals query.


## Rentals

```graphql
query rentals($ids: [ID!]!) {
    rentals(ids: $ids) {
        __typename
        id
        anyrooms
        anyrooms_description
        bedrooms
        bedrooms_description
        baths_short_description
        baths_description
        is_featured
        listed_price
        title_with_unit
        medium_image_uri
        large_image_uri
        unit_type
        url
        source
        building {
            __typename
            id
        }
        address {
            __typename
            pretty_address
            unit
        }
        area {
            __typename
            id
            name
        }
        contacts {
            __typename
            id
            name
            phone
            account_url
            business_name
            full_business_address
            industry_professional {
                __typename
                id
            }
            license {
                __typename
                id
                display_type
            }
        }
        open_houses {
            __typename
            id
        }
    }
}
```

## Buildings

```graphql
query buildings($ids: [ID!]!) {
    buildings(ids: $ids) {
        id
        url
        active_listings_count
        building_type
        landmark_name
        medium_image_uri
        residential_unit_count
        year_built
        __typename
        address {
            pretty_address      
            __typename
        }
        area { 
            name      
            __typename
        }
    }
}
```