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

# Command line handle input
def main() -> None:

    #If arguments not equal to 3, print debug message and exit 
    if len(sys.argv) != 3:
        print("Please use: Lab_7P.py www.google.com google.html")
        sys.exit(1)

    host: str = sys.argv[1]
    port: int = 80
    fileName: str = sys.argv[2]
    bufferSize = 1024 * 512
    response: bytes = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
    html_content = getResponse(host, port, bufferSize, response)
    
    result = writeFile(html_content, fileName)
    print(result)

if __name__ == "__main__":
    main()
