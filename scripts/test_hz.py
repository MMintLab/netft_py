import argparse
import time

from netft_py import NetFT


def test_hz(ip: str, duration: float = 5.0):
    netft = NetFT(ip)
    netft.startStreaming()

    time.sleep(duration)

    print(f"Frequency over {duration} seconds: {netft.get_frequency()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test API frequency.")
    parser.add_argument("ip", type=str, help="IP address of the Net F/T sensor.")
    parser.add_argument("--duration", "-d", type=float, default=5.0, help="Duration to test frequency (seconds).")
    args = parser.parse_args()

    test_hz(args.ip, args.duration)
