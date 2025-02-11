def validate_ipv4(ip):
    parts = ip.split(".")

    if len(parts) != 4:
        return "Invalid IP format. Must be in the format xxx.xxx.xxx.xxx (0-255)."

    for part in parts:
        if not part.isdigit():
            return f"Invalid IP: '{part}' is not a number."
        if not 0 <= int(part) <= 255:
            return f"Invalid IP: '{part}' is out of range (0-255)."
        #if part != str(int(part)):  
            #return f"Invalid IP: '{part}' should not have leading zeros."

    return f"Valid IPv4 address: {ip} ({classify_ip(ip)})"

def classify_ip(ip):
    first, second, *_ = map(int, ip.split("."))

    if (first == 10) or \
       (first == 172 and 16 <= second <= 31) or \
       (first == 192 and second == 168):
        return "Private IP"
    else:
        return "Public IP"

def validate_gmail(email):
    if "@gmail.com" not in email:
        return "Invalid email: Must be a Gmail address (ends with @gmail.com)."

    username, domain = email.rsplit("@", 1) 

    if domain != "gmail.com":
        return "Invalid email: Domain must be 'gmail.com'."

    allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789._"
    for char in username:
        if char not in allowed_chars:
            return f"Invalid email: Character '{char}' is not allowed in the username."

    return f"Valid Gmail address: {email}"

if __name__ == "__main__":
    ip = input("Enter an IPv4 address: ")
    email = input("Enter a Gmail address: ")

    print(validate_ipv4(ip))
    print(validate_gmail(email))
