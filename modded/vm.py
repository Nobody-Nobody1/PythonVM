import socket
import struct
import subprocess

# --- Settings ---
WIDTH = 127
HEIGHT = 127
FPS = 60

OPCODES = {
    "load": "6c6f6164",
    "plus": "706c7573",
    "take": "74616b65",
    "keep": "6b656570",
    "jump": "6a756d70",
    "halt": "68616c74",
}

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
            os_logic(registers, stack, program_counter, os_string_buffer, os_frame_buffer)

            if DEBUG:
                input ("Press ENTER to go to the next state")
                print("PC:", program_counter, "REG:", registers, "STACK:", stack)

def os_logic(registers, stack, program_counter, os_string_buffer, os_frame_buffer):
    # User Programs can use R0 to R239
    # OS reserved is the rest from R240 to R255
    # R255 toggles OS logic behaviour
    # R254 is the syscall for the kernel to use
    # R253 is what to get for syscalls
    # R252 are more options if needed with the syscall
    # R251 is X for pixel
    # R250 is Y for pixel
    # R249 is color value for pixel
    # R248 is for selecting which graphics mode to use

    # Syscalls
    kerneltoggle = registers.get(255, 0)
    kernelsyscall = registers.get(254, 0)
    kernelsyscallargument1 = registers.get(253, 0)
    kernelsyscallargument2 = registers.get(252, 0)

    # Graphics
    pixelx = registers.get(251, 0)
    pixely = registers.get(250, 0)
    pixelcolor = registers.get(249, 0)
    index_type = registers.get(248, 0)

    if kerneltoggle == 1: # toggle for os syscalls
        #print("OS KERNEL ACTIVATED") for debugging when it starts

        if kernelsyscall == 1: # add letter to buffer
            register = registers.get(kernelsyscallargument1, 0) # register to add
            letter = chr(register)
            os_string_buffer.append(letter)

        if kernelsyscall == 2: # print os buffer
            string = "".join(os_string_buffer)
            print(string)

        elif kernelsyscall == 3: # reads user input
            register = registers.get(kernelsyscallargument1, 0) # register to read and output keyboard input to it
            value = input("Enter a value for R" + str(register) + ": ") # the value from user
            registers[register] = int(value)

        elif kernelsyscall == 4: # add pixel to buffer
            index = graphics_mode_select(index_type, pixelx, pixely)
            if 0 <= index < len(os_frame_buffer):
                os_frame_buffer[index] = pixelcolor
            else:
                print("Pixel out of bounds:", pixelx, pixely, "-> index", index)
        
        elif kernelsyscall == 5:
            # serve viewer as server
            with socket.create_server(("127.0.0.1", 9000)) as server:
                print("Server on port 9000...")
                conn, addr = server.accept()
                with conn:
                    frame_size = WIDTH * HEIGHT
                    header = struct.pack("Q", frame_size)
                    conn.sendall(header)
                    conn.sendall(os_frame_buffer)

        registers[255] = 0

def graphics_mode_select(index_type, pixelx, pixely):
    if index_type == 0:
        index = pixely * WIDTH + pixelx
    elif index_type == 1: 
        index = pixelx * pixely
    elif index_type == 2:
        index = (pixelx ^ pixely)
    elif index_type == 3:
        index = (pixelx & pixely)
    elif index_type == 4:
        index = (pixelx | pixely)
    elif index_type == 5:
        index = (pixelx + pixely)
    elif index_type == 6:
        index = abs(pixelx - pixely)
    elif index_type == 7:
        index = (pixelx * pixely) ^ pixelx
    elif index_type == 8:
        index = (pixelx * pixely) + pixelx
    elif index_type == 9:
        index = (pixelx * pixely) % (WIDTH * HEIGHT)
    elif index_type == 10:
        index = pixely * WIDTH
    elif index_type == 11:
        index = pixelx * HEIGHT
    elif index_type == 12:
        index = (pixelx + pixely) % 2
    return index