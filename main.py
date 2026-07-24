import assembler as assembler # assembler
import vanilla.vm as vanillavm # vanilla program logic
import modded.vm as moddedvm # modded program logic

os_dev = True # determines if making the os where os specific logic is there along with regular logic

def main(dev):
    #regular program
    source = "vanilla/regular.vasm"
    binary = "vanilla/regular.bin"

    #os specific program
    os_source = "modded/os.vasm"
    os_binary = "modded/os.bin"

    if dev:
        print("Assembling Modded Program...")
        assembler.assemble(os_source, os_binary)
        print("Running Modded VM...")
        moddedvm.run(os_binary) # runs the modded logic for os dev

    else:
        print("Assembling Vanilla Program...")
        assembler.assemble(source, binary)
        print("Running Vanilla VM...")
        vanillavm.run(binary) # runs the vanilla code logic

if __name__ == "__main__":
    main(os_dev)