# emulator.py
# GUI wrapper around assembler.py and vm.py
# Shows screen + console + register panel (0–255, negative registers mapped)

import customtkinter as ctk
import threading
import assembler
import vm


class Emulator(ctk.CTk):

    def __init__(self, binary_path):
        super().__init__()

        self.title("EditOS VM Emulator")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.binary_path = binary_path
        self.running = False
        self.run_thread = None
        self.vm_state = None

        # --------------------------------------------------------
        # LAYOUT
        # --------------------------------------------------------
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --------------------------------------------------------
        # LEFT SIDE: SCREEN + CONSOLE
        # --------------------------------------------------------
        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.screen_canvas = ctk.CTkCanvas(
            left, width=320, height=320,
            bg="black", highlightthickness=0
        )
        self.screen_canvas.pack(padx=10, pady=10)

        self.console_box = ctk.CTkTextbox(left, height=200)
        self.console_box.pack(fill="x", padx=10, pady=(0, 10))

        # --------------------------------------------------------
        # RIGHT SIDE: REGISTERS + BUTTONS
        # --------------------------------------------------------
        right = ctk.CTkFrame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right.grid_rowconfigure(1, weight=1)

        controls = ctk.CTkFrame(right)
        controls.grid(row=0, column=0, pady=10)

        self.run_btn = ctk.CTkButton(controls, text="Run", width=120, command=self.start_run)
        self.run_btn.grid(row=0, column=0, padx=10)

        self.pause_btn = ctk.CTkButton(controls, text="Pause", width=120, command=self.pause_run)
        self.pause_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = ctk.CTkButton(controls, text="Reset", width=120, command=self.reset_vm)
        self.reset_btn.grid(row=0, column=2, padx=10)

        # --------------------------------------------------------
        # SCROLLABLE REGISTER PANEL (0–255)
        # --------------------------------------------------------
        self.register_frame = ctk.CTkScrollableFrame(right, width=250)
        self.register_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.register_labels = []
        for r in range(256):
            label = ctk.CTkLabel(self.register_frame, text=f"R{r:03}: 0")
            label.pack(anchor="w")
            self.register_labels.append(label)

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
        for r in range(256):
            self.register_labels[r].configure(text=f"R{r:03}: 0")
        self.vm_state = None

    def run_vm(self):
        import builtins
        original_print = builtins.print

        def capture_print(*args, **kwargs):
            text = " ".join(str(a) for a in args)
            self.console_box.insert("end", text + "\n")
            self.console_box.see("end")

        builtins.print = capture_print

        self.vm_state = vm.run(self.binary_path)

        builtins.print = original_print
        self.running = False

    # --------------------------------------------------------
    # UI UPDATE LOOP
    # --------------------------------------------------------

    def update_ui(self):
        if self.vm_state:
            regs = self.vm_state["registers"]

            # Start with all registers 0–255 = 0
            mapped = {r: 0 for r in range(256)}

            # Fill in positive registers normally
            for r, val in regs.items():
                if r >= 0:
                    mapped[r] = val

            # Map negative registers directly:
            # -1 → 255, -2 → 254, etc.
            for r, val in regs.items():
                if r < 0:
                    mapped[(r + 256) % 256] = val

            # Update labels
            for r in range(256):
                self.register_labels[r].configure(text=f"R{r:03}: {mapped[r]}")

        self.after(200, self.update_ui)


# --------------------------------------------------------
# MAIN
# --------------------------------------------------------

def main():
    source = "emulator.vasm"
    binary = "emulator.bin"

    print("Assembling...")
    assembler.assemble(source, binary)

    print("Launching Emulator...")
    app = Emulator(binary)
    app.mainloop()


if __name__ == "__main__":
    main()