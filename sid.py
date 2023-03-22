sid = "121356486"
if sid is None or sid == "":
    sid = input("Enter your student ID: ")

first_6_digits = int(sid[0:6])
last_5_digits = int(sid[-5:])
hash = (first_6_digits // last_5_digits)+ (first_6_digits % last_5_digits)
print(hash)