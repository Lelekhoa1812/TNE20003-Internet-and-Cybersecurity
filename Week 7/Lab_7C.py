import socket
import sys

# Get HTTP response method
def getResponse(host: str, port: int, bufferSize: int, request: bytes) -> str:
   
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
        return f"{fileName}already exists!"
    except Exception as e:
        return f"An error occurred when write file: {str(e)}"
    
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
        print(f"Can not display content: {response_code}")

# Command line handle input
def main() -> None:

    #If arguments not equal to 3, print debug message and exit 
    if len(sys.argv) != 3:
        print("Please use: Lab_7C.py www.google.com google2.html")
        sys.exit(1)

    host: str = sys.argv[1]
    port: int = 80
    fileName: str = sys.argv[2]
    bufferSize = 1024 * 512
    response: bytes = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
    http_response = getResponse(host, port, bufferSize, response)

    parsed_response = parseResponse(http_response)
    displayResponse(parsed_response)
    result = writeFile(parsed_response[3], fileName)
    print(result)

if __name__ == "__main__":
    main()
