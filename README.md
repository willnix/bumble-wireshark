# Bumble Wireshark Live Capture

This setup allows **live streaming of Bumble Bluetooth HCI traffic into Wireshark** using a FIFO and Wireshark’s **extcap** interface.
Bumble writes HCI packets in the **PCAP (DLT_BLUETOOTH_HCI_H4_WITH_DIR)** format, and Wireshark decodes them in real time.

No files are written. Everything is streamed.

---

## What this does

```
Bumble -> FIFO -> extcap -> Wireshark
```

* Bumble emits HCI packets into a named pipe
* extcap forwards the pipe into Wireshark
* Wireshark shows a live Bluetooth trace with correct directions

---

## Files

### `snoop.py`

This is a patched Bumble snoop.py that adds a ``pcapsnoooper`` which writes PCAP (HCI H4 with direction) to a FIFO.

Place it in:

```
bumble/snoop.py
```

Overwrite the existing file.

I have opened a [PR](https://github.com/google/bumble/pull/865) for bumble so this step may become obsolete.

---

### `extcap-bumble.py`

This is a Wireshark extcap helper that forwards the FIFO to Wireshark.

Place it in:

```
~/.local/lib/wireshark/extcap/extcap-bumble.py
```

Then make it executable:

```
chmod +x ~/.local/lib/wireshark/extcap/extcap-bumble.py
```

Restart Wireshark after installing it.

---

## Running

1. Start Wireshark
   Select the **Bumble HCI** interface and click **Start Capture**.

2. Start Bumble with the snooper enabled:

```
BUMBLE_SNOOPER=pcapsnoop:pipe:/tmp/bumble-extcap uv run example.py
```

Packets will appear in Wireshark immediately.

NOTE: You can freely set the FIFO path here, but for now its hardcoded in ``extcap-bumble.py``.

---

## Notes

* Wireshark must be started before Bumble so the FIFO is open.
* The capture uses PCAP with `DLT_BLUETOOTH_HCI_H4_WITH_DIR`, so packet direction is shown correctly.
* This works for both BLE and BR/EDR traffic.
* This will not work on Windows because:
   * Python does not support named pipes on Windows out-of-the-box
   * Python files are not runnable on Windows, so the extcap script would need a .bat wrapper
