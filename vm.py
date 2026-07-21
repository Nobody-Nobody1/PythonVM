file = "program"

with open(file + ".bin", "rb") as binary:
    for line in binary:
        print(binary.read())