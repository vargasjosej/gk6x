#!/usr/bin/env python3
"""
GK6X GUI Simple - Versión simplificada que funciona en Kinoite
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
from pathlib import Path

class SimpleGK6XGui:
    def __init__(self, root):
        self.root = root
        self.root.title("GK6X Configurator")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Paths
        self.app_dir = Path(__file__).parent
        self.gk6x_exe = self.app_dir / "source_code" / "Build" / "GK6X.exe"
        
        # Check mono
        self.mono_available = self.check_mono()
        
        self.create_ui()
    
    def check_mono(self):
        try:
            result = subprocess.run(["mono", "--version"], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def create_ui(self):
        # Title
        title = tk.Label(self.root, text="GK6X Keyboard Configurator",
                        font=("Arial", 18, "bold"), bg='#2b2b2b', fg='#00ff88')
        title.pack(pady=20)
        
        # Status
        status_text = "✅ Mono available" if self.mono_available else "⚠️ Mono not installed"
        status = tk.Label(self.root, text=status_text,
                         font=("Arial", 10), bg='#2b2b2b', fg='white')
        status.pack()
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg='#2b2b2b')
        btn_frame.pack(pady=30)
        
        buttons = [
            ("📝 Apply Config (Map)", self.map_keyboard),
            ("🔄 Reset (Unmap)", self.unmap_keyboard),
            ("📋 List Keys", self.dump_keys),
        ]
        
        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                           font=("Arial", 12), bg='#3c3c3c', fg='white',
                           padx=20, pady=10, relief='flat',
                           activebackground='#00ff88')
            btn.pack(pady=5, fill='x')
        
        # Console
        console_label = tk.Label(self.root, text="Console Output:",
                                font=("Arial", 10, "bold"),
                                bg='#2b2b2b', fg='white')
        console_label.pack(pady=(20, 5))
        
        self.console = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, height=15,
            font=("Courier", 9), bg='#000000', fg='#00ff00'
        )
        self.console.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Initial message
        self.log("GK6X Configurator started")
        self.log(f"Mono available: {self.mono_available}")
        if not self.mono_available:
            self.log("WARNING: Install mono with: toolbox run sudo dnf install mono-core")
    
    def log(self, message):
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
        self.root.update_idletasks()
    
    def run_command(self, args):
        if not self.mono_available:
            messagebox.showerror("Error", "Mono is not installed!")
            return
        
        if not self.gk6x_exe.exists():
            messagebox.showerror("Error", f"GK6X.exe not found at: {self.gk6x_exe}")
            return
        
        try:
            self.log(f"\nRunning: mono {self.gk6x_exe} {' '.join(args)}")
            
            process = subprocess.Popen(
                ["mono", str(self.gk6x_exe)] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.gk6x_exe.parent)
            )
            
            stdout, stderr = process.communicate(timeout=10)
            
            if stdout:
                self.log(stdout)
            if stderr:
                self.log(f"ERROR: {stderr}")
            
            if process.returncode == 0:
                self.log("✓ Command completed successfully")
            else:
                self.log(f"✗ Command failed with code: {process.returncode}")
                
        except subprocess.TimeoutExpired:
            process.kill()
            self.log("ERROR: Command timed out")
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
    
    def map_keyboard(self):
        if messagebox.askyesno("Confirm", "Apply configuration?"):
            self.run_command(["/map"])
    
    def unmap_keyboard(self):
        if messagebox.askyesno("Confirm", "Reset to default?"):
            self.run_command(["/unmap"])
    
    def dump_keys(self):
        self.run_command(["/dumpkeys"])

def main():
    print("Starting Simple GK6X GUI...")
    root = tk.Tk()
    app = SimpleGK6XGui(root)
    print("GUI initialized, starting mainloop")
    root.mainloop()
    print("GUI closed")

if __name__ == "__main__":
    main()
