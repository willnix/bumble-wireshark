#!/usr/bin/env python3
import sys, os, tempfile

def arg(name):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return None

def main():
    if "--extcap-interfaces" in sys.argv:
        print("extcap {version=1.0}")
        print("interface {value=bumble}{display=Bumble HCI}")
        return

    if "--extcap-dlts" in sys.argv:
        print("dlt {number=201}{name=DLT_BLUETOOTH_HCI_H4_WITH_PHDR}{display=Bluetooth HCI H4}")
        return

    if "--capture" in sys.argv:
        wireshark_fifo = arg("--fifo")

        # create FIFO that Bumble will write into
        bumble_fifo = "/tmp/bumble-extcap"
        try:
            os.mkfifo(bumble_fifo)
            os.chmod(bumble_fifo, 0o666)
        except FileExistsError:
            pass

        print("Waiting for Bumble to connect...", file=sys.stderr)

        # forward Bumble -> Wireshark
        fd = os.open(bumble_fifo, os.O_RDONLY | os.O_NONBLOCK)
        src = os.fdopen(fd, "rb", buffering=0)

        with src, open(wireshark_fifo, "wb") as dst:
            while True:
                data = src.read(4096)
                if not data:
                    continue
                dst.write(data)
                dst.flush()

        return

if __name__ == "__main__":
    main()
