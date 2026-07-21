file = "program"

OPCODES = {
    "load": "6c6f6164",
    "plus": "706c7573",
    "take": "74616b65",
    "keep": "6b656570",
    "jump": "6a756d70",
    "halt": "68616c74",
}

with open(file + ".bin", "rb") as binary:
    program_counter = 0
    registers = {}
    stack = []
    max_cycles = 10000
    cycles = 0

    while cycles < max_cycles:
        cycles += 1
        binary.seek(program_counter)
        instr = binary.read(6)

        if not instr or len(instr) != 6:
            break

        opcode = instr[0:4].hex()
        op1 = instr[4]
        op2 = instr[5]

        # auto-init registers
        if op1 not in registers:
            registers[op1] = 0
        if op2 not in registers:
            registers[op2] = 0

        if opcode == OPCODES["load"]:
            registers[op1] = op2
            program_counter += 6

        elif opcode == OPCODES["plus"]:
            registers[op1] += registers[op2]
            program_counter += 6

        elif opcode == OPCODES["take"]:
            registers[op1] -= registers[op2]
            program_counter += 6

        elif opcode == OPCODES["keep"]:
            stack.append(registers[op1])
            program_counter += 6

        elif opcode == OPCODES["jump"]:
            # op1 = number of instructions to jump
            # op2 = register containing condition
            if registers[op2] > 0:
                program_counter -= registers[op1] * 6
            else:
                program_counter += 6


        elif opcode == OPCODES["halt"]:
            print("reached halt")
            break

        print("HEX:", opcode)
        print("OPCODE:", opcode)
        print("OPERANDS:", op1, op2)
        print("REGISTERS:", registers)
        print("STACK:", stack)
        print("COUNTER:", program_counter)
        print()