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

## Abstract Syntax Tree

In the AST folder, the method of using abstract syntax trees to find the difference between parsers is explored. The file parser_diff.py is a similarity checker that has extracted the core functionality of the Python package Pycode_similar. It includes two methods to calculate the similarity between two functions:
- UnifiedDiff: Finds the difference in nodes after normalising the function's nodes.
- TreeDiff: Uses the package zss.distance to find the distance between two ordered trees, which is considered to be the weighted number of edit operations to transform one tree to  another.

At the bottom of the file is an example of how the code can be used to find the similarity.
