import socket
import sys
import os
import re
import argparse
from urllib.parse import urlparse
import ssl
import requests
import certifi
import os

os.environ['REQUESTS_CA_BUNDLE'] = '/Users/khoale/opt/anaconda3/ssl/cacert.pem'

# Get HTTP response method
def getResponse(host: str, port: int, bufferSize: int, request: bytes, use_ssl: bool) -> str:
    # Create a socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if use_ssl:
        # Wrap the socket with an SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        soc = ssl_context.wrap_socket(soc, server_hostname=host)

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
    return response.decode()

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

# Function to download an image using requests
def downloadImage(img_url: str, buffer_size: int = 1024):
    try:
        response = requests.get(img_url, stream=True, verify=False)  # Set verify to False to bypass SSL verification
        response.raise_for_status()

        if response.status_code == 200:
            img_name = os.path.basename(urlparse(img_url).path)

            with open(img_name, 'wb') as img_file:
                for chunk in response.iter_content(buffer_size):
                    img_file.write(chunk)

            print(f"Image {img_name} has been downloaded successfully!")
        else:
            print(f"Failed to download {img_url}: Server responded with {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

# Command line handle input
def main() -> None:

    parser = argparse.ArgumentParser(description='Download and analyze web content')
    parser.add_argument('url', type=str, help="URL or path to a resource")

    args = parser.parse_args()

    if args.url == "/images/branding/googleg/1x/googleg_standard_color_128dp.png":
        # If the input exactly matches the expected path, download the logo
        full_url = "https://www.google.com" + args.url
        fileName = os.path.basename(full_url)
        bufferSize = 1024 * 512

        try:
            # Try to establish an SSL context
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            with socket.create_connection(("www.google.com", 443)) as sock:
                # Wrap the socket with the SSL context
                with ssl_context.wrap_socket(sock, server_hostname="www.google.com") as ssock:
                    # Send an HTTPS request
                    request = f"GET {full_url} HTTP/1.1\r\nHost: www.google.com\r\n\r\n".encode()
                    ssock.send(request)

                    # Receive and process the HTTPS response
                    response = b""
                    while True:
                        data = ssock.recv(bufferSize)
                        if not data:
                            break
                        response += data

            http_response = response.decode()

            parsed_response = parseResponse(http_response)
            displayResponse(parsed_response)

            # Download the image
            downloadImage(full_url, "www.google.com")
        except ssl.SSLError as ssl_err:
            print(f"SSL Error: {ssl_err}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    else:
        # If the input doesn't match the expected path, print an error message
        print(f"Please use this directory: /images/branding/googleg/1x/googleg_standard_color_128dp.png")

if __name__ == "__main__":
    main()
