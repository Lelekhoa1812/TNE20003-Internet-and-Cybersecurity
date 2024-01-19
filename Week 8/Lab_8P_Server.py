import socket
import argparse


def serverListener(host: str, port: int, bufferSize: int = 1024) -> None:
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_soc.bind((host, port))

    while True:
        data, address = server_soc.recvfrom(bufferSize)
        message = data.decode('ascii')

        if not message.startswith("TNE20003:"):
            error_message = f"TNE20003:E:Invalid Protocol Header: {message}"
            server_soc.sendto(error_message.encode('ascii'), address)
            continue

        payload = message[9:]

        if not payload:
            error_message = "TNE20003:E:Empty Messsage"
            server_soc.sendto(error_message.encode('ascii'), address)
            continue

        ack_message = f"TNE20003:A:{payload}"
        server_soc.sendto(ack_message.encode('ascii'), address)


def main() -> None:
    arg_parser = argparse.ArgumentParser("Server UDP")
    arg_parser.add_argument(
        "-host", help="Client host, default localhost", default="127.0.0.1", type=str)
    arg_parser.add_argument(
        "-port", help="Client port, default 4231", default=4231, type=int)
    arg_parser.add_argument(
        "-bufferSize", help="Buffer size, default 1024", default=1024, type=int)
    args = arg_parser.parse_args()
    serverListener(args.host, args.port, args.bufferSize)


if __name__ == "__main__":
    main()
