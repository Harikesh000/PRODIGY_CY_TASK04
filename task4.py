import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from datetime import datetime

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.is_running = False
        self.listener = None

        # Ask for permission at startup
        self.ask_permission()

        self._build_ui()

    def ask_permission(self):
        answer = messagebox.askyesno(
            "Permission Required",
            "This app will log your keystrokes with timestamps into a file.\n\n"
            "Do you give permission to proceed?"
        )
        if not answer:
            messagebox.showinfo("Permission Denied", "Keylogger will not run without consent.")
            self.root.destroy()  # close the app if denied

    def _build_ui(self):
        title = tk.Label(self.root, text="Keylogger", font=("Times New Roman", 18, "bold"))
        title.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Paused", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Run", width=10, command=self.start_logging).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Pause", width=10, command=self.stop_logging).pack(side=tk.LEFT, padx=10)

        # Live log viewer
        self.log_display = tk.Text(self.root, height=12, width=60, state=tk.DISABLED, bg="#f0f0f0")
        self.log_display.pack(pady=10)

    def start_logging(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Status: Running", fg="green")
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

    def stop_logging(self):
        if self.is_running:
            self.is_running = False
            self.status_label.config(text="Status: Paused", fg="red")
            if self.listener:
                self.listener.stop()

    def on_press(self, key):
        if self.is_running:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                key_str = key.char
            except AttributeError:
                key_str = f"[{key}]"

            log_entry = f"{timestamp} - {key_str}\n"

            # Save to file
            with open("keylog.txt", "a") as f:
                f.write(log_entry)

            # Show in GUI
            self.log_display.config(state=tk.NORMAL)
            self.log_display.insert(tk.END, log_entry)
            self.log_display.see(tk.END)
            self.log_display.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
