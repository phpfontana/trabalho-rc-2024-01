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

string = "BANANA"
um, dois = string.split(" ", 1)
print(um, dois)
