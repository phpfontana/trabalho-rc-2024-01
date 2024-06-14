def to_lowercase_bytes(byte_array:bytearray) -> bytearray:
    for i in range(len(byte_array)):
        if 65 <= byte_array[i] <= 90:
            byte_array[i] += 32
    return byte_array

def is_utf8_compatible(byte_array:bytearray) -> bool:
    try:
        byte_array.decode()
        return True
    except UnicodeError as _:
        return False
