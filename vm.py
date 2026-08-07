from assembler import OPCODES
from os_logic import handle_syscalls

# --- Settings ---
WIDTH = 127
HEIGHT = 127
FPS = 60

DEBUG = False

def run(binary_file):
    program_counter = 0
    registers = {}
    stack = []
    os_string_buffer = []
    os_frame_buffer = bytearray(WIDTH * HEIGHT)
    max_cycles = 1000000
    cycles = 0

    with open(binary_file, "rb") as binary:
        while cycles < max_cycles:
            cycles += 1
            binary.seek(program_counter)
            instr = binary.read(6)

            if not instr or len(instr) != 6:
                break

            opcode = instr[0:4].hex()
            op1 = instr[4]
            op2 = instr[5]

            # decode signed bytes for negative values in operand 2
            if op2 >= 128:
                op2 -= 256

            if op1 not in registers:
                registers[op1] = 0
            if opcode != OPCODES["load"] and op2 not in registers:
                registers[op2] = 0

            if opcode == OPCODES["load"]:
                registers[op1] = op2
                program_counter += 6

            elif opcode == OPCODES["plus"]:
                registers[op1] = (registers[op1] + registers[op2]) % 256
                program_counter += 6

            elif opcode == OPCODES["take"]:
                registers[op1] = (registers[op1] - registers[op2]) % 256
                program_counter += 6

            elif opcode == OPCODES["keep"]:
                stack.append(registers[op1])
                program_counter += 6

            elif opcode == OPCODES["jump"]:
                if registers[op2] > 0:
                    if registers[op1] >= 0:
                        program_counter += registers[op1] * 6
                    else:
                        program_counter -= abs(registers[op1]) * 6
                else:
                    program_counter += 6

            elif opcode == OPCODES["halt"]:
                break

            # OS specific logic
            handle_syscalls(registers, stack, program_counter, os_string_buffer, os_frame_buffer, WIDTH, HEIGHT)

            if DEBUG:
                input ("Press ENTER to go to the next state")
                print("PC:", program_counter, "REG:", registers, "STACK:", stack)