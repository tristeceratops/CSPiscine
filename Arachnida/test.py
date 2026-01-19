import struct

# -----------------------------
# Config / Tag definitions
# -----------------------------
EXIF_TAGS = {
    0x829A: "ExposureTime",   # Rational
    0x829D: "FNumber",        # Rational
    0x8827: "ISO",            # Short
    0x9201: "ShutterSpeedValue",  # Rational
    0x9209: "Flash",          # Short
    0x0131: "Software",       # ASCII
}

# TIFF data types
TIFF_TYPES = {
    1: ("BYTE", 1),
    2: ("ASCII", 1),
    3: ("SHORT", 2),
    4: ("LONG", 4),
    5: ("RATIONAL", 8),
    7: ("UNDEFINED", 1),
    9: ("SLONG", 4),
    10: ("SRATIONAL", 8),
}

# -----------------------------
# Low-level EXIF parser
# -----------------------------
def read_exif_subifd(jpeg_path):
    with open(jpeg_path, "rb") as f:
        data = f.read()

    # 1️⃣ Find EXIF APP1 marker
    start = data.find(b"Exif\x00\x00")
    if start == -1:
        print("No EXIF found")
        return

    tiff_header_start = start + 6
    tiff_header = data[tiff_header_start:]

    # 2️⃣ Determine endianness
    endian_flag = tiff_header[0:2]
    if endian_flag == b'II':
        endian = '<'  # little endian
    elif endian_flag == b'MM':
        endian = '>'  # big endian
    else:
        print("Unknown endianness")
        return

    # 3️⃣ Offset to 0th IFD
    ifd0_offset = struct.unpack(endian + 'L', tiff_header[4:8])[0]
    ifd0_start = tiff_header_start + ifd0_offset
    num_entries_0th = struct.unpack(endian + 'H', data[ifd0_start:ifd0_start+2])[0]

    # 4️⃣ Search for Exif SubIFD pointer (tag 0x8769)
    subifd_offset = None
    for i in range(num_entries_0th):
        entry_start = ifd0_start + 2 + i * 12
        tag, type_, count, value_offset = struct.unpack(endian + 'HHLL', data[entry_start:entry_start+12])
        if tag == 0x8769:
            subifd_offset = tiff_header_start + value_offset
            break

    if not subifd_offset:
        print("No Exif SubIFD found")
        return

    # 5️⃣ Read SubIFD entries
    num_entries_subifd = struct.unpack(endian + 'H', data[subifd_offset:subifd_offset+2])[0]
    exif_data = {}

    for i in range(num_entries_subifd):
        entry_start = subifd_offset + 2 + i * 12
        tag, type_, count, value_offset = struct.unpack(endian + 'HHLL', data[entry_start:entry_start+12])

        if tag not in EXIF_TAGS:
            continue

        dtype, dsize = TIFF_TYPES.get(type_, ("UNKNOWN", 1))
        total_size = count * dsize

        if total_size <= 4:
            # value stored directly
            raw_bytes = struct.pack(endian + 'L', value_offset)[:total_size]
        else:
            val_start = tiff_header_start + value_offset
            raw_bytes = data[val_start:val_start + total_size]

        # Decode depending on type
        if dtype == "ASCII":
            value = raw_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
        elif dtype == "RATIONAL":
            # assume count = 1 for simplicity
            numerator, denominator = struct.unpack(endian + 'LL', raw_bytes)
            value = numerator / denominator if denominator != 0 else 0
            print(f"{numerator}/{denominator}")
        elif dtype == "SHORT":
            value = struct.unpack(endian + 'H', raw_bytes)[0]
        elif dtype == "LONG":
            value = struct.unpack(endian + 'L', raw_bytes)[0]
        else:
            value = raw_bytes

        exif_data[EXIF_TAGS[tag]] = value

    # 6️⃣ Print results
    for key, val in exif_data.items():
        print(f"{key}: {val}")


# -----------------------------
# Example usage
# -----------------------------
read_exif_subifd("photo.jpg")
