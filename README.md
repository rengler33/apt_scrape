# apt_scrape - Apartment Scraper

This project is merely for fun and may become out of date. I have no reason for keeping it working (see note below). 

It may include additional sites at later dates.

## StreetEasy rental scraping
StreetEasy is an apartment rental site focused on New York City.

NOTE: There is no reason to use this scraper: StreetEasy will send instant notifications on new listings that match desired criteria. But I've never scraped a GraphQL API before, so when I noticed that this site makes a decent amount of info available there, I decided to play around with exploring anyway.

### Notes
The site is generally server-side rendered. Rather than crawl the pagination of the site, it is possible to retrieve the high-level details of a listing using their internal GraphQL API (if the rental IDs are known). The GraphQL API is used by the site mainly when navigating map views. 


### GraphQL Queries
There are two queries created: `rental` and `building`. 

### Search criteria
When collecting the rental IDs of interest, it's possible to specify the search criteria in the URL. (note: %7C is the pipe |)

```
https://streeteasy.com/for-rent/brooklyn/price:1000-5000%7Csqft%3E=600%7Cbeds:1-2%7Cbaths%3E=1%7Camenities:pets,washer_dryer,dishwasher,private_outdoor_space
```