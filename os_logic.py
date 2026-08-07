import socket
import struct

__all__ = ["handle_syscalls"]

def handle_syscalls(registers, stack, program_counter, os_string_buffer, os_frame_buffer, WIDTH, HEIGHT):
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
            index = _graphics_mode_select(index_type, pixelx, pixely, WIDTH)
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

def _graphics_mode_select(index_type, pixelx, pixely, WIDTH):
    if index_type == 0:
        index = pixely * WIDTH + pixelx
    elif index_type == 1: 
        index = pixelx * pixely
    return index