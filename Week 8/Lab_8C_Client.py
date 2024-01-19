import socket
import argparse

def clientListener(host: str, port: int, bufferSize: int = 1024) -> None:
    client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_soc.connect((host, port))
    except ConnectionRefusedError:
        print(f"Error: Connection to {host}:{port} refused.")
        return

    while True:
        message = input("Enter message to Server ('exit' to quit): ")

        if message.lower() == 'exit':
            break

        if message.startswith("TNE20003: "):
            client_soc.sendall(message.encode('ascii'))
            data = client_soc.recv(bufferSize)
            if not data:
                print("Server disconnected.")
                break
            print(f"Received from Server: {data.decode('ascii')}")
        else:
            print("Error: Message format is invalid. It should start with 'TNE20003: '")

    client_soc.close()

def main() -> None:
    arg_parser = argparse.ArgumentParser("Client TCP")
    arg_parser.add_argument(
        "-host", help="Server host, default localhost", default="127.0.0.1", type=str)
    arg_parser.add_argument(
        "-port", help="Server port, default 4231", default=4231, type=int)
    arg_parser.add_argument(
        "-bufferSize", help="Buffer size, default 1024", default=1024, type=int)
    args = arg_parser.parse_args()
    clientListener(args.host, args.port, args.bufferSize)

if __name__ == "__main__":
    main()
