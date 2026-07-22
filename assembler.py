OPCODES = {
    "load": "6c6f6164",
    "plus": "706c7573",
    "take": "74616b65",
    "keep": "6b656570",
    "jump": "6a756d70",
    "halt": "68616c74",
}

def assemble(src, out):
    with open(src, "r") as program, open(out, "wb") as binary:
        for line in program:
            line = line.strip()
            if not line or line.startswith(";"):
                continue

            # Remove comments
            line = line.split(";")[0].strip()
            parts = line.split()
            opcode = parts[0]
            operands = parts[1:]

            opcode_bytes = bytes.fromhex(OPCODES[opcode])

            # ----------------------------------------------------
            # operand 1 (register or immediate)
            # ----------------------------------------------------
            if operands:
                op1 = operands[0].replace(",", "")
                if op1.startswith("R"):
                    reg1 = int(op1[1:])     # FULL NUMBER (fix)
                else:
                    reg1 = int(op1)
            else:
                reg1 = 0

            # ----------------------------------------------------
            # operand 2 (register or immediate)
            # ----------------------------------------------------
            if len(operands) > 1:
                op2 = operands[1].replace(",", "")
                if op2.startswith("R"):
                    reg2 = int(op2[1:])     # FULL NUMBER (fix)
                else:
                    reg2 = int(op2)
            else:
                reg2 = 0

            # ----------------------------------------------------
            # Encode signed bytes (wrap into 0–255)
            # ----------------------------------------------------
            reg1 &= 0xFF
            reg2 &= 0xFF

            # ----------------------------------------------------
            # Write 6-byte instruction
            # ----------------------------------------------------
            binary.write(opcode_bytes)
            binary.write(bytes([reg1]))
            binary.write(bytes([reg2]))

    print("Assembled:", out)