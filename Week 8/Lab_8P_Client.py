import socket
import argparse


def clientListener(host: str, port: int, bufferSize: int = 1024) -> None:
    client_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = input("Enter message to Server ('exit' to quit): ")

        if message.lower() == 'exit':
            break

        client_soc.sendto(f"TNE20003:{message}".encode('ascii'), (host, port))

        data, address = client_soc.recvfrom(bufferSize)
        print(f"Received from Client {address}: {data.decode('ascii')}")
    client_soc.close()


def main() -> None:
    arg_parser = argparse.ArgumentParser("Client UDP")
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
