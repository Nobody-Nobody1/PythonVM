import assembler
import vm

def main():
    source = "program.vasm"
    binary = "program.bin"

    print("Assembling...")
    assembler.assemble(source, binary)

    print("Running VM...")
    vm.run(binary)

if __name__ == "__main__":
    main()