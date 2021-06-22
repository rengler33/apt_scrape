# Queries
Queries of https://api-internal.streeteasy.com/graphql

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