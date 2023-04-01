# Baidu Image Crawler

A simple and efficient Python script to scrape images from Baidu Image Search based on a specified keyword. The script supports downloading large amounts of images while avoiding anti-crawler mechanisms.

## Features

- Download images from Baidu Image Search by keyword
- Specify the number of images to download
- Multi-threaded downloading for faster performance
- Automatically avoids anti-crawler mechanisms
- Randomized user agent and delays between requests

## Requirements

- Python 3.x
- `requests`
- `fake_useragent`

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/baidu-image-crawler.git
```
Install the required packages:
```bash
pip install -r requirements.txt
```
Usage
```bash
python baidu_image_crawler.py
```
Modify the keyword and num_images variables in the script to specify the keyword for image search and the number of images to download.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
MIT
