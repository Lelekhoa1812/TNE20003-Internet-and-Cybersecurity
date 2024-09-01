import socket
import sys
import os
import re
import argparse
from urllib.parse import urlparse
import requests

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
def parseResponse(http_response: bytes):
    # Split the response into HTTP header and HTML content
    header, html_content = http_response.split(b'\r\n\r\n', 1)

    # Split the HTTP header into lines
    header_lines = header.decode('utf-8').split('\r\n')

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

def writeFile(response: bytes, fileName: str = "GetResponse.json") -> str:
    try:
        with open(fileName, "wb") as file:  # Open the file in binary write mode
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

def extractImage(http_content: bytes) -> list:
    try:
        http_content_str = http_content.decode('utf-8')
        img_tags = re.findall(r'<img[^>]+src=["\'](http://[^"\']+)', http_content_str)
        return img_tags
    except UnicodeDecodeError:
        return []


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
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()

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

# Command line input
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
        # Construct a GET request for the image URL
        custom_request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        response = custom_request.encode()
        bufferSize = 1024 * 512
        http_response = getResponse(host, port, bufferSize, response)

        parsed_response = parseResponse(http_response)
        displayResponse(parsed_response)

        # Since it's an image URL, you don't need to extract image tags or download further.
        # Just save the image directly.
        img_url = args.url
        downloadImage(img_url, host)

        # You can specify a custom file name if needed, e.g., "googlelogo.png"
        # downloadImage(img_url, host, buffer_size=1024, file_name="googlelogo.png")
    else:
        # Download and save images
        downloadImage(args.url, host)

if __name__ == "__main__":
    main()
