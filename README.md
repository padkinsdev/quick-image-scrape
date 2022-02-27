# Quick Image Scraper

## What it is
This repo is a quick script that I threw together for the purpose of scraping images from a webpage. Theoretically, it downloads all of the images on a given webpage to a folder, with the option to pass in multiple pages to scrape

## Dependencies
This script requires BeautifulSoup4 (`pip3 install bs4`) and Requests (`pip3 install requests`), and it relies heavily on their functionality.

## Flags
Two flags may be given for this script: `-path` and `new-folder`. Using `-path=<path to download folder>` will cause the script to save images to the specified path if it is valid. Otherwise the current working directory will be used for saving images. Using `-new-folder=true` or `-new-folder=True` will result in the script creating a new folder in the path specified by the `-path` flag in order to save images. Otherwise, images will be saved directly to the specified path.

## Caveats
Note that the script is rather verbose and at times downloads the same images multiple times because it does not check if it has requested an image already when iteration through the list of image urls. Additionally, the script uses the `time.sleep()`, `random.random()`, and `round()` methods to delay each image request by part of a second per iteration in order to avoid being rate limited by the website, and more importantly to not cause a strain on the website. As a result, the script may work slower than you prefer.

## Final thoughts
Hopefully this is of use to others. It's not meant to be sophisticated or comprehensive, but it definitely beats right clicking every image you want to save. Have fun!
