file = "program"

with open(file + ".bin", "rb") as binary:
    while True:
        instr = binary.read(6)
        if not instr:
            break
        if len(instr) != 6:
            raise MemoryError("Malformed instruction: not 6 bytes")
        print(instr)
