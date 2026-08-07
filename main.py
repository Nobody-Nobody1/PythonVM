import assembler as assembler # assembler
import vm as moddedvm # modded program logic

def main():
    source = "program.vasm"
    binary = "program.bin"

    print("Assembling Program...")
    assembler.assemble(source, binary)
    print("Running Modded VM...")
    moddedvm.run(binary) # runs the modded logic for os dev

if __name__ == "__main__":
    main()