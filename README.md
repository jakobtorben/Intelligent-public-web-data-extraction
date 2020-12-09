# Intelligent-public-web-data-extraction
Imperial College London Advanced Data Science Team - Intelligent public web data extraction project with Refinitiv

To run the spider first clone the repository:

```
git clone https://github.com/jakobtorben/Intelligent-public-web-data-extraction
cd ManWebScraper
```

to run the HSBC crawler run the command

```
scrapy crawl extract_board -o HSBC_board.csv
```

Similarly for Unilever

```
scrapy crawl Unilever_board -o Unilever_board.csv
```
