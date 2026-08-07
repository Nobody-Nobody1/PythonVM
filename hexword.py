import pyperclip

def to_hex(word: str) -> str:
    hexcode = word.encode("ascii").hex()
    return f'"{word}": "{hexcode}",'

if __name__ == "__main__":
    text = input("Enter opcode word: ")
    text_to_copy = to_hex(text)
    pyperclip.determine_clipboard()
    pyperclip.copy(text_to_copy)
    print(text_to_copy)