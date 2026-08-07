import assembler as assembler # assembler
import vm as moddedvm # modded program logic

def main():
    os_source = "program.vasm"
    os_binary = "program.bin"

    print("Assembling Modded Program...")
    assembler.assemble(os_source, os_binary)
    print("Running Modded VM...")
    moddedvm.run(os_binary) # runs the modded logic for os dev

if __name__ == "__main__":
    main()