#!/usr/bin/env python3
"""
GK6X GUI - Modern GUI for GK6X Keyboard Configuration
Fixed version for Fedora Kinoite
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import os
import sys
import threading
from pathlib import Path

class GK6XGui:
    def __init__(self, root):
        self.root = root
        self.root.title("GK6X Keyboard Configurator")
        self.root.geometry("900x700")
        
        # Paths
        self.app_dir = Path(__file__).parent
        self.gk6x_exe = self.app_dir / "source_code" / "Build" / "GK6X.exe"
        self.userdata_dir = self.app_dir / "source_code" / "Build" / "UserData"
        
        # Check if mono is available
        self.mono_available = self.check_mono()
        
        # Variables
        self.connected_device = tk.StringVar(value="Not connected")
        self.current_config = tk.StringVar(value="")
        
        # Set theme BEFORE creating widgets
        self.setup_theme()
        
        # Create UI
        self.create_menu()
        self.create_main_ui()
        
        # Check for device on startup (delayed)
        self.root.after(1000, self.check_device)
    
    def setup_theme(self):
        """Setup modern theme"""
        try:
            style = ttk.Style()
            
            # Use clam theme safely
            available_themes = style.theme_names()
            if 'clam' in available_themes:
                style.theme_use('clam')
            
            # Custom colors
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            accent_color = "#00ff88"
            
            # Configure styles
            style.configure(".", background=bg_color, foreground=fg_color)
            style.configure("TLabel", background=bg_color, foreground=fg_color)
            style.configure("TButton", background="#3c3c3c", foreground=fg_color, 
                           borderwidth=1, relief="flat", padding=6)
            style.map("TButton", background=[("active", accent_color)])
            style.configure("TFrame", background=bg_color)
            style.configure("TNotebook", background=bg_color, borderwidth=0)
            style.configure("TNotebook.Tab", background="#3c3c3c", foreground=fg_color, 
                           padding=[10, 5])
            style.map("TNotebook.Tab", 
                     background=[("selected", accent_color)],
                     foreground=[("selected", "#000000")])
        except Exception as e:
            print(f"Theme setup warning: {e}")
    
    def check_mono(self):
        """Check if mono is installed"""
        try:
            result = subprocess.run(["mono", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Config", command=self.load_config)
        file_menu.add_command(label="Save Config", command=self.save_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Dump Keys", command=self.dump_keys)
        tools_menu.add_command(label="Find Keys", command=self.find_keys)
        tools_menu.add_command(label="Check Device", command=self.check_device)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)
    
    def create_main_ui(self):
        """Create main UI"""
        # Top frame - Status
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(status_frame, text="Device Status:", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(status_frame, textvariable=self.connected_device,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(status_frame, text="🔄 Refresh", 
                  command=self.check_device).pack(side=tk.RIGHT, padx=5)
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Quick Actions
        quick_tab = ttk.Frame(notebook)
        notebook.add(quick_tab, text="Quick Actions")
        self.create_quick_actions_tab(quick_tab)
        
        # Tab 2: Config Editor
        config_tab = ttk.Frame(notebook)
        notebook.add(config_tab, text="Config Editor")
        self.create_config_editor_tab(config_tab)
        
        # Tab 3: Console Output
        console_tab = ttk.Frame(notebook)
        notebook.add(console_tab, text="Console")
        self.create_console_tab(console_tab)
        
        # Tab 4: Web GUI
        webgui_tab = ttk.Frame(notebook)
        notebook.add(webgui_tab, text="Web GUI")
        self.create_webgui_tab(webgui_tab)
    
    def create_quick_actions_tab(self, parent):
        """Create quick actions tab"""
        # Description
        desc_frame = ttk.Frame(parent)
        desc_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(desc_frame, text="Quick Keyboard Configuration",
                 font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(desc_frame, 
                 text="Use these buttons to quickly configure your GK6X keyboard",
                 font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Map button
        map_btn = ttk.Button(buttons_frame, text="📝 Apply Configuration (Map)",
                            command=self.map_keyboard)
        map_btn.pack(fill=tk.X, pady=5)
        
        ttk.Label(buttons_frame, 
                 text="Applies your custom keyboard configuration",
                 font=("Arial", 8)).pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Unmap button
        unmap_btn = ttk.Button(buttons_frame, text="🔄 Reset to Default (Unmap)",
                              command=self.unmap_keyboard)
        unmap_btn.pack(fill=tk.X, pady=5)
        
        ttk.Label(buttons_frame,
                 text="Resets keyboard to factory default settings",
                 font=("Arial", 8)).pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Dump Keys button
        dump_btn = ttk.Button(buttons_frame, text="📋 List Keys (Dump Keys)",
                             command=self.dump_keys)
        dump_btn.pack(fill=tk.X, pady=5)
        
        ttk.Label(buttons_frame,
                 text="Shows all key names and their positions",
                 font=("Arial", 8)).pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Find Keys button
        find_btn = ttk.Button(buttons_frame, text="🔍 Identify Keys (Find Keys)",
                             command=self.find_keys)
        find_btn.pack(fill=tk.X, pady=5)
        
        ttk.Label(buttons_frame,
                 text="Tool to identify key names and find broken keys",
                 font=("Arial", 8)).pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Status info
        if not self.mono_available:
            warning_label = ttk.Label(buttons_frame,
                text="⚠️ Warning: mono is not installed. Install it with: sudo dnf install mono-complete",
                font=("Arial", 9, "bold"),
                foreground="#ff6666")
            warning_label.pack(pady=20)
    
    def create_config_editor_tab(self, parent):
        """Create config editor tab"""
        # Toolbar
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(toolbar, text="📁 Load", 
                  command=self.load_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="💾 Save", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📝 New", 
                  command=self.new_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📄 Sample", 
                  command=self.load_sample).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(toolbar, text="Current:", 
                 font=("Arial", 9)).pack(side=tk.LEFT, padx=(20, 5))
        ttk.Label(toolbar, textvariable=self.current_config,
                 font=("Arial", 9, "italic")).pack(side=tk.LEFT)
        
        # Text editor
        editor_frame = ttk.Frame(parent)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.config_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff"
        )
        self.config_editor.pack(fill=tk.BOTH, expand=True)
        
        # Add default help text
        help_text = """# GK6X Configuration File
# Lines starting with # are comments
# 
# Basic key mapping: KEY_NAME=KEY_CODE
# Example: A=B  (A key will output B)
#
# Macros: KEY_NAME={KEY1,KEY2,KEY3}
# Example: F1={LControl,C}  (F1 will Ctrl+C)
#
# Layers: Use Layer1, Layer2, Layer3 sections
# Example:
# [Layer1]
# A=B
#
# For more examples, click "Sample" button above
"""
        self.config_editor.insert("1.0", help_text)
    
    def create_console_tab(self, parent):
        """Create console output tab"""
        # Console output
        self.console = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            height=30,
            font=("Courier", 9),
            bg="#000000",
            fg="#00ff00",
            insertbackground="#00ff00"
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Clear button
        ttk.Button(parent, text="Clear Console", 
                  command=lambda: self.console.delete(1.0, tk.END)).pack(pady=5)
        
        self.log("GK6X GUI started successfully")
        self.log(f"Mono available: {self.mono_available}")
        self.log(f"GK6X executable: {self.gk6x_exe}")
    
    def create_webgui_tab(self, parent):
        """Create web GUI tab"""
        desc_frame = ttk.Frame(parent)
        desc_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(desc_frame, text="Web-Based GUI",
                 font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(desc_frame,
                 text="Launch the web-based interface for visual keyboard configuration",
                 font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        # Info
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        info_text = """
The Web GUI provides a visual interface for configuring your keyboard.

To use the Web GUI:
1. Click "Start Web GUI" below
2. Your web browser will open automatically
3. The interface will be available at http://localhost:6464
4. Configure your keyboard visually
5. Close this application when done

Note: The web GUI has some limitations. The text-based config editor
is more powerful and reliable for advanced configurations.
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=10)
        
        # Start button
        self.webgui_btn = ttk.Button(info_frame, text="🌐 Start Web GUI",
                                     command=self.start_webgui)
        self.webgui_btn.pack(pady=20)
        
        self.webgui_status = tk.StringVar(value="Not running")
        ttk.Label(info_frame, text="Status:", 
                 font=("Arial", 10, "bold")).pack()
        ttk.Label(info_frame, textvariable=self.webgui_status,
                 font=("Arial", 10)).pack()
    
    def log(self, message):
        """Log message to console"""
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
        self.root.update_idletasks()
    
    def run_gk6x_command(self, args, callback=None):
        """Run GK6X command"""
        if not self.mono_available:
            messagebox.showerror("Error", 
                "Mono is not installed. Please install it with:\nsudo dnf install mono-complete")
            return
        
        if not self.gk6x_exe.exists():
            messagebox.showerror("Error",
                f"GK6X executable not found at: {self.gk6x_exe}")
            return
        
        def run():
            try:
                self.log(f"Running: mono {self.gk6x_exe} {' '.join(args)}")
                
                process = subprocess.Popen(
                    ["mono", str(self.gk6x_exe)] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=str(self.gk6x_exe.parent)
                )
                
                # Read output
                stdout, stderr = process.communicate(timeout=30)
                
                if stdout:
                    for line in stdout.split('\n'):
                        if line:
                            self.log(line)
                
                if stderr:
                    for line in stderr.split('\n'):
                        if line:
                            self.log(f"ERROR: {line}")
                
                if process.returncode == 0:
                    self.log("Command completed successfully")
                else:
                    self.log(f"Command failed with exit code: {process.returncode}")
                
                if callback:
                    callback(process.returncode == 0)
                    
            except subprocess.TimeoutExpired:
                process.kill()
                self.log("ERROR: Command timed out")
                if callback:
                    callback(False)
            except Exception as e:
                self.log(f"Exception: {str(e)}")
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def check_device(self):
        """Check for connected device"""
        self.connected_device.set("Checking...")
        
        def callback(success):
            if success:
                # Parse output for device info
                output = self.console.get("1.0", tk.END)
                lines = output.split("\n")
                for line in lines:
                    if "Connected to device" in line:
                        device_info = line.split("Connected to device")[1].strip()
                        self.connected_device.set(device_info)
                        return
                self.connected_device.set("Device found")
            else:
                self.connected_device.set("No device detected")
        
        # Just run without args to check connection
        self.run_gk6x_command([], callback)
    
    def map_keyboard(self):
        """Apply keyboard configuration"""
        if messagebox.askyesno("Confirm", 
            "This will apply your configuration to the keyboard. Continue?"):
            self.log("\n=== Applying Configuration ===")
            self.run_gk6x_command(["/map"])
    
    def unmap_keyboard(self):
        """Reset keyboard to default"""
        if messagebox.askyesno("Confirm",
            "This will reset your keyboard to default settings. Continue?"):
            self.log("\n=== Resetting to Default ===")
            self.run_gk6x_command(["/unmap"])
    
    def dump_keys(self):
        """Dump keyboard keys"""
        self.log("\n=== Dumping Keys ===")
        self.run_gk6x_command(["/dumpkeys"])
    
    def find_keys(self):
        """Find/identify keys"""
        self.log("\n=== Finding Keys ===")
        self.run_gk6x_command(["/findkeys"])
    
    def start_webgui(self):
        """Start web GUI"""
        self.log("\n=== Starting Web GUI ===")
        self.webgui_status.set("Starting...")
        
        def callback(success):
            if success:
                self.webgui_status.set("Running on http://localhost:6464")
                # Try to open browser
                import webbrowser
                webbrowser.open("http://localhost:6464")
            else:
                self.webgui_status.set("Failed to start")
        
        self.run_gk6x_command(["/gui"], callback)
    
    def load_config(self):
        """Load config file"""
        filename = filedialog.askopenfilename(
            title="Load Config",
            initialdir=self.userdata_dir if self.userdata_dir.exists() else ".",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.config_editor.delete(1.0, tk.END)
                self.config_editor.insert(1.0, content)
                self.current_config.set(Path(filename).name)
                self.log(f"Loaded config: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def save_config(self):
        """Save config file"""
        filename = filedialog.asksaveasfilename(
            title="Save Config",
            initialdir=self.userdata_dir if self.userdata_dir.exists() else ".",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                content = self.config_editor.get(1.0, tk.END)
                with open(filename, 'w') as f:
                    f.write(content)
                self.current_config.set(Path(filename).name)
                self.log(f"Saved config: {filename}")
                messagebox.showinfo("Success", "Configuration saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def new_config(self):
        """Create new config"""
        if messagebox.askyesno("New Config", 
            "Create a new configuration? Unsaved changes will be lost."):
            self.config_editor.delete(1.0, tk.END)
            self.current_config.set("Untitled")
    
    def load_sample(self):
        """Load sample config"""
        sample_file = self.userdata_dir / "Sample.txt"
        if sample_file.exists():
            try:
                with open(sample_file, 'r') as f:
                    content = f.read()
                self.config_editor.delete(1.0, tk.END)
                self.config_editor.insert(1.0, content)
                self.current_config.set("Sample.txt")
                self.log(f"Loaded sample config")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load sample: {str(e)}")
        else:
            messagebox.showerror("Error", f"Sample file not found: {sample_file}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """GK6X Keyboard Configurator
Version 1.0

A modern GUI for configuring GK6X keyboards
(GK61, GK64, GK84, etc.)

Based on the GK6X project by pixeltris
https://github.com/pixeltris/GK6X

Created with Python and Tkinter
License: MIT
"""
        messagebox.showinfo("About", about_text)
    
    def show_docs(self):
        """Show documentation"""
        docs_text = """GK6X Documentation

Quick Start:
1. Connect your GK6X keyboard
2. Check device status (it should auto-detect)
3. Use Quick Actions or Config Editor to configure
4. Apply configuration with "Map" button

Configuration File Format:
- Lines starting with # are comments
- Key mapping: KEY=VALUE
- Macros: KEY={KEY1,KEY2,...}
- Layers: Use [Layer1], [Layer2], [Layer3] sections

For more info, visit:
https://github.com/pixeltris/GK6X
"""
        messagebox.showinfo("Documentation", docs_text)

def main():
    """Main entry point"""
    try:
        print("Starting GK6X GUI (Full Version)...")
        root = tk.Tk()
        print("Root window created")
        app = GK6XGui(root)
        print("App initialized, entering mainloop")
        root.mainloop()
        print("GUI closed")
        return 0
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
