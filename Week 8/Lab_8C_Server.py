import socket
import argparse
import threading

def serverListener(host: str, port: int, bufferSize: int = 1024) -> None:
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_soc.bind((host, port))
    server_soc.listen(5)

    try:
        while True:
            print("Server listening for connections...")
            client_soc, addr = server_soc.accept()
            print(f"Accepted connection from {addr}")

            client_handler = threading.Thread(target=handle_client, args=(client_soc, bufferSize))
            client_handler.start()

    except KeyboardInterrupt:
        print("Server terminated.")
    finally:
        server_soc.close()

def handle_client(client_soc, bufferSize):
    while True:
        data = client_soc.recv(bufferSize)
        if not data:
            break

        message = data.decode('ascii')

        if not message.startswith("TNE20003:"):
            error_message = f"TNE20003:E:Invalid Protocol Header: {message}"
            client_soc.send(error_message.encode('ascii'))
            continue

        payload = message[9:]

        if not payload:
            error_message = "TNE20003:E:Empty Message"
            client_soc.send(error_message.encode('ascii'))
            continue

        ack_message = f"TNE20003:A:{payload}"
        client_soc.send(ack_message.encode('ascii'))

    client_soc.close()

def main() -> None:
    arg_parser = argparse.ArgumentParser("Server TCP")
    arg_parser.add_argument(
        "-host", help="Server host, default localhost", default="127.0.0.1", type=str)
    arg_parser.add_argument(
        "-port", help="Server port, default 4231", default=4231, type=int)
    arg_parser.add_argument(
        "-bufferSize", help="Buffer size, default 1024", default=1024, type=int)
    args = arg_parser.parse_args()
    serverListener(args.host, args.port, args.bufferSize)

if __name__ == "__main__":
    main()
