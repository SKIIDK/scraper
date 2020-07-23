# scraper

## Spider
To run the scraper, from the spiders directory use `scrapy runspider scrape.py`. The current default method is set to get all files, but it can also be configured to only get MIFR files. All of the reports will be saved to the reports folder.

## XML Parsing
To run the xml parser, run `./xmlformat.py <file-path>`. This will output the domains file for the corresponding XML file.