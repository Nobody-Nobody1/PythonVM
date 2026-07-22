# emulator.py
# Clean GUI wrapper around assembler.py and vm.py
# Only shows screen + console + 3 centered buttons

import customtkinter as ctk
import threading
import assembler
import vm


class Emulator(ctk.CTk):

    def __init__(self, binary_path):
        super().__init__()

        self.title("EditOS VM Emulator")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.binary_path = binary_path
        self.running = False
        self.run_thread = None

        # --------------------------------------------------------
        # MAIN LAYOUT
        # --------------------------------------------------------
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # --------------------------------------------------------
        # SCREEN (top)
        # --------------------------------------------------------
        self.screen_canvas = ctk.CTkCanvas(
            self, width=320, height=320,
            bg="black", highlightthickness=0
        )
        self.screen_canvas.grid(row=0, column=0, pady=(20, 10))

        # --------------------------------------------------------
        # CONSOLE (middle)
        # --------------------------------------------------------
        self.console_box = ctk.CTkTextbox(self, height=150)
        self.console_box.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="n")

        # --------------------------------------------------------
        # BUTTONS (bottom, centered)
        # --------------------------------------------------------
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, pady=20)

        self.run_btn = ctk.CTkButton(button_frame, text="Run", width=120, command=self.start_run)
        self.run_btn.grid(row=0, column=0, padx=10)

        self.pause_btn = ctk.CTkButton(button_frame, text="Pause", width=120, command=self.pause_run)
        self.pause_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = ctk.CTkButton(button_frame, text="Reset", width=120, command=self.reset_vm)
        self.reset_btn.grid(row=0, column=2, padx=10)

        # UI update loop
        self.after(200, self.update_ui)

    # --------------------------------------------------------
    # VM CONTROL
    # --------------------------------------------------------

    def start_run(self):
        if not self.running:
            self.running = True
            self.run_thread = threading.Thread(target=self.run_vm, daemon=True)
            self.run_thread.start()

    def pause_run(self):
        self.running = False

    def reset_vm(self):
        self.console_box.delete("1.0", "end")
        self.screen_canvas.delete("all")

    def run_vm(self):
        import builtins
        original_print = builtins.print

        def capture_print(*args, **kwargs):
            text = " ".join(str(a) for a in args)
            self.console_box.insert("end", text + "\n")
            self.console_box.see("end")

        builtins.print = capture_print
        vm.run(self.binary_path)
        builtins.print = original_print

        self.running = False

    # --------------------------------------------------------
    # UI UPDATE LOOP
    # --------------------------------------------------------

    def update_ui(self):
        # Screen drawing can be added later when vm exposes registers
        self.after(200, self.update_ui)


# --------------------------------------------------------
# MAIN (same structure as your main.py)
# --------------------------------------------------------

def main():
    source = "program.vasm"
    binary = "program.bin"

    print("Assembling...")
    assembler.assemble(source, binary)

    print("Launching Emulator...")
    app = Emulator(binary)
    app.mainloop()


if __name__ == "__main__":
    main()