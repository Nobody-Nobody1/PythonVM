OPCODES = {
    "load": "6c6f6164",
    "plus": "706c7573",
    "take": "74616b65",
    "keep": "6b656570",
    "jump": "6a756d70",
    "halt": "68616c74",
}

DEBUG = False
STEP_MODE = False

def run(binary_file):
    program_counter = 0
    registers = {r: 0 for r in range(256)}   # full unsigned register set
    stack = []
    max_cycles = 10000
    cycles = 0

    with open(binary_file, "rb") as binary:
        while cycles < max_cycles:
            cycles += 1
            binary.seek(program_counter)
            instr = binary.read(6)

            if not instr or len(instr) != 6:
                break

            opcode = instr[0:4].hex()
            op1 = instr[4]          # now ALWAYS 0–255
            op2 = instr[5]          # now ALWAYS 0–255

            # ----------------------------------------------------
            # INSTRUCTIONS
            # ----------------------------------------------------

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
                # jump only if condition register > 0
                if registers[op2] > 0:
                    offset = registers[op1]
                    program_counter += offset * 6
                else:
                    program_counter += 6

            elif opcode == OPCODES["halt"]:
                break

            if STEP_MODE:
                input("Press Enter to step...")

            if DEBUG or STEP_MODE:
                print("PC:", program_counter, "REG:", registers, "STACK:", stack)

    return {
        "pc": program_counter,
        "registers": registers,
        "stack": stack,
        "cycles": cycles
    }