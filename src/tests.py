def handle_data(line):
    if line.startswith("NICK"):
        handle_nickname(line)

    elif line.startswith('USER'):
        print("Handling USER\n")

def handle_nickname(line):
    parts = line.split()
    print("Logs:")
    print(f"Command: {parts}")
    
    pass

buffer = ""
data = "NICK test01\r\nUSER test02\r\n"
buffer += data

while '\r\n' in buffer:
    line, buffer = buffer.split('\r\n', 1)
    print(f"\nLogs:")
    print(f"Line: {line}\n")
    handle_data(line)
    