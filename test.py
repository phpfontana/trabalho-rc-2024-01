message = ":<host> 366 <username> #<canal> :End of /NAMES list."


message = message.split(" ", 3)[3]
print(message)