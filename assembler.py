file = "program"

#only supports 4 byte opcodes (all opcodes are designed to be only 4 bytes) and 2 operands are supported only for minimalism
with open(file + ".vasm", "r") as program, open(file + ".bin", "wb") as binary:
    for line in program:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        opcode = parts[0]
        operands = parts[1:]

        # 1. opcode → 4 ASCII bytes
        opcode_bytes = opcode.encode("ascii")

        # 2. operand1 (always a register)
        if operands:
            reg1 = int(operands[0][1])   # "R0," → 0
        else:
            reg1 = 0

        # 3. operand2 (register OR immediate OR none)
        if len(operands) > 1:
            op2 = operands[1].replace(",", "")
            if op2.startswith("R"):
                reg2 = int(op2[1])       # register
            else:
                reg2 = int(op2)          # immediate
        else:
            reg2 = 0

        # 4. write 6 bytes
        binary.write(opcode_bytes)
        binary.write(bytes([reg1]))
        binary.write(bytes([reg2]))