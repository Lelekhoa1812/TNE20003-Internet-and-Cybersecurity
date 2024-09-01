import socket
import sys
import os
import re
import argparse
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Get HTTP response method
def getResponse(host: str, port: int, bufferSize: int, request: bytes) -> bytes:
    # Create a socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((host, port))

    # Send HTTP request, receive and accumulate responses
    soc.send(request)
    response: bytes = b""
    while True:
        data = soc.recv(bufferSize)
        if not data:
            break
        response += data

    soc.close()
    return response

# Parse HTTP response method
def parseResponse(http_response: str):
    # Split the response into HTTP header and HTML content
    header, html_content = http_response.split('\r\n\r\n', 1)

    # Split the HTTP header into lines
    header_lines = header.split('\r\n')

    # Extract response code and message
    status_line = header_lines[0].split(' ', 2)
    response_code = status_line[1]
    response_message = status_line[2]

    # Extract and store header content in a dictionary
    headers_dict = {}
    for line in header_lines[1:]:
        key, value = line.split(': ', 1)
        headers_dict[key] = value

    return response_code, response_message, headers_dict, html_content

# Write file method
def writeFile(response: str, fileName: str = "GetResponse.json") -> str:
    try:
        with open(fileName, "w") as file:
            file.write(response)
            return f"{fileName} has been created!"
    except FileExistsError:
        return f"{fileName} already exists!"
    except Exception as e:
        return f"An error occurred when writing the file: {str(e)}"

# Display Response method
def displayResponse(parsed_response: tuple) -> None:
    response_code, response_message, headers_dict, html_content = parsed_response
    print(f"HTTP Response Code: {response_code}")
    print(f"HTTP Response Message: {response_message}")
    print(f"HTTP Content:")
    for key, value in headers_dict.items():
        print(f"{key}: {value}")

    # Response HTTP = 200?
    if response_code == '200':
        print("\nHTML Content:")
        print(html_content)
    else:
        print(f"Cannot display content: {response_code}")

# Function to extract image tags from HTML content
def extractImage(http_content: str) -> list:
    img_tags = re.findall(r'<img[^>]+src=["\'](http://[^"\']+)', http_content)
    return img_tags

# Function to download an image using socket
def downloadImage(img_url: str, host: str, buffer_size: int = 1024) -> None:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if img_url.startswith("http://"):
        match = re.match(r'http://([^/]+)(/.*)', img_url)
        if not match:
            print(f"Ignore invalid URL: {img_url}")
            return
        host, path = match.groups()
    else:
        if img_url.startswith("/"):
            path = img_url
        else:
            path = f"/{img_url}"
    img_name = os.path.basename(path)
    request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()

    try:
        soc.connect((host, 80))
        soc.send(request)
        response = b""
        while True:
            data = soc.recv(buffer_size)
            if not data:
                break
            response += data
    except Exception as exception:
        print(f"Failed to retrieve data {img_url}: {exception}")
        return

    header, img_data = response.split(b'\r\n\r\n', 1)
    if b"200 OK" in header:
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Image {img_name} has been downloaded successfully!")
    else:
        print(
            f"Failed to download {img_url}: Server responded with {header.split(b' ', 2)[1]}")

def scrape_images(url):
    try:
        # Send an HTTP GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find image tags and extract image URLs
            img_tags = soup.find_all('img')
            img_urls = [img.get('src') for img in img_tags]

            return img_urls
        else:
            print(f"Failed to retrieve data from {url}: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
    return []

# Command line handle input
def main() -> None:
    parser = argparse.ArgumentParser(description='Download and analyze web content')
    parser.add_argument('url', type=str, help="URL of the resource to download")

    args = parser.parse_args()

    url_parts = urlparse(args.url)
    host = url_parts.netloc
    path = url_parts.path

    if not host:
        print(f"Invalid URL: {args.url}")
        return

    port = 80  # HTTP port

    if args.url.startswith("http://"):
        # If it's an HTTP web page URL, perform the existing operations
        response = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
        bufferSize = 1024 * 512
        http_response = getResponse(host, port, bufferSize, response)

        parsed_response = parseResponse(http_response)
        displayResponse(parsed_response)

        # Extract image tags from HTML content using the new function
        img_tags = extractImage(parsed_response[3])

        # Download and save images
        if img_tags:
            downloadImage(img_tags[0], host)

        # Scrape and print image URLs using the new function
        scraped_img_urls = scrape_images(args.url)
        if scraped_img_urls:
            print("\nScraped Image URLs:")
            for img_url in scraped_img_urls:
                print(img_url)

        fileName = 'image.html'
        result = writeFile(parsed_response[3], fileName)
        print(result)
    else:
        # Download and save images
        downloadImage(args.url, host)

if __name__ == "__main__":
    main()