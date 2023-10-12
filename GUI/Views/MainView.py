import tkinter as tk
from tkinter import filedialog
import os

class MainView(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.create_widgets()
        self.grid(row=0, column=1, sticky="nswe")

    def create_widgets(self):
        def ask_input_file():
            file = filedialog.askopenfilename(filetypes=[("Kismet DB", ".kismet")])
            if file:
                self.ent_input_browse.config(state="normal")
                self.ent_input_browse.delete(0, tk.END)
                self.ent_input_browse.insert(0, file)
                self.ent_input_browse.config(state="disabled")
                self.ent_output_browse.config(state="normal")
                self.ent_output_browse.delete(0, tk.END)
                if self.v_compress_kml.get():
                    self.ent_output_browse.insert(0, f"{file}.kmz")
                else:
                    self.ent_output_browse.insert(0, f"{file}.kml")
                self.ent_output_browse.config(state="disabled")
        
        def ask_output_file():
            file = filedialog.asksaveasfilename(filetypes=[("KML", ".kml"),("KMZ", ".kmz")])
            if file:
                self.ent_output_browse.config(state="normal")
                self.ent_output_browse.delete(0, tk.END)
                self.ent_output_browse.insert(0, file)
                check_compress_kml()
                self.ent_output_browse.config(state="disabled")
        
        def check_compress_kml():
            if not self.ent_output_browse.get():
                return
            else:
                file_name, file_ext = os.path.splitext(self.ent_output_browse.get())
                if file_ext in (".kml", ".kmz"): # prevent doubling the extensions, allows the use of periods in filename
                    file_ext = ''
                if self.v_compress_kml.get():
                    file = f"{file_name}{file_ext}.kmz"
                else:
                    file = f"{file_name}{file_ext}.kml"
                self.ent_output_browse.config(state="normal")
                self.ent_output_browse.delete(0, tk.END)
                self.ent_output_browse.insert(0, file)
                self.ent_output_browse.config(state="disabled")
                
        # Create frames to group related widgets
        frm_input_file = tk.LabelFrame(self, text="Input (Kismet DB)")
        frm_output_file = tk.LabelFrame(self, text="Output (KML)")
        
        # Build the widgets for the input file
        lbl_input_browse = tk.Label(frm_input_file, text="File Path:")
        self.ent_input_browse = tk.Entry(frm_input_file, width=75, state="readonly")
        btn_input_browse = tk.Button(frm_input_file, text="Browse...", command=ask_input_file)
                
        # Build the widgets for the output file
        frm_output_filename = tk.Frame(frm_output_file)
        lbl_output_browse = tk.Label(frm_output_file, text="File Path:")
        self.ent_output_browse = tk.Entry(frm_output_filename, width=75, state="readonly")
        btn_output_browse = tk.Button(frm_output_filename, text="Browse...", command=ask_output_file)
        # Add a checkbox, checked by default, to compress the KML
        self.v_compress_kml = tk.BooleanVar()
        chk_compress_kml = tk.Checkbutton(frm_output_file, text="Compress KML (to KMZ)", command=check_compress_kml, variable=self.v_compress_kml)
        chk_compress_kml.select()
        # Add a checkbox, unchecked by default, to create a heatworm
        self.v_heatworm = tk.BooleanVar()
        chk_heatworm = tk.Checkbutton(frm_output_file, text="Create Heatworm", variable=self.v_heatworm)
        
        # Build the wdiget for the status box
        console = tk.Frame(self, borderwidth=1, relief="sunken")
        self.console_text = tk.Text(console, wrap="none", width=70, height=5)
        console_Vsb = tk.Scrollbar(console, orient="vertical", command=self.console_text.yview)
        console_Hsb = tk.Scrollbar(console, orient="horizontal", command=self.console_text.xview)
        self.console_text.configure(yscrollcommand=console_Vsb.set, xscrollcommand=console_Hsb.set)
        self.console_text.grid(row=0, column=0, sticky="nsew")
        console_Vsb.grid(row=0, column=1, sticky="ns")
        console_Hsb.grid(row=1, column=0, sticky="ew")
        
        # Build the widgets for convert button
        self.btn_convert = tk.Button(self, text="Convert")
        
        # input widgets grid placement
        lbl_input_browse.grid(row=0, column=0, padx=(3,0), pady=(5,0), sticky="nw")
        self.ent_input_browse.grid(row=0, column=1, padx=(5,5), pady=(5,0), ipady=2, sticky="nw")
        btn_input_browse.grid(row=0, column=2, padx=(0,5), pady=(0,5), ipadx=2, sticky="nw")

        # output widgets grid placement
        lbl_output_browse.grid(row=0, column=0, padx=(3,0), pady=(5,0), sticky="nw")
        self.ent_output_browse.grid(row=0, column=1, padx=(5,5), pady=(5,0), ipady=2, sticky="nw")
        btn_output_browse.grid(row=0, column=2, padx=(0,5), pady=(0,5), ipadx=2, sticky="nw")
        frm_output_filename.grid(row=0, column=1, sticky="nw")
        chk_compress_kml.grid(row=1, column=1, sticky="nw")
        chk_heatworm.grid(row=2, column=1, sticky="nw")
        
        # input/output frame group and convert button grid placement
        frm_input_file.grid(row=0, column=0, padx=(5,5), pady=(0,0), sticky="nsew")
        frm_output_file.grid(row=1, column=0, padx=(5,5), pady=(0,0), sticky="nsew")
        
        # grid placement for convert button, progress bar and console
        self.btn_convert.grid(row=2, column=0, padx=(5,5), pady=(5,5), ipadx=10, ipady=5)
        console.grid(row=3, column=0, padx=(5,5), pady=(5,5), sticky="nsew")