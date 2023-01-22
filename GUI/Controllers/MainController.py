# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from threading import Thread
import queue

from GUI.Models import MainModel
from GUI.Views import MainView

class MainController():
    def __init__(self, root):
        self.root = root
        self.model = MainModel()
        self.view = MainView(root)
        self.view.btn_convert.bind("<Button-1>", self.start_conversion)

    def start_conversion(self, _):
        q = queue.Queue()
        
        def after_callback():
            try:
                message = q.get(block=False)
                if message is not None:
                    self.view.console_text.insert(tk.END, message + '\n')
                    self.view.console_text.see(tk.END) # Scroll down as new lines are added
                    self.root.after(100, after_callback)
                else:
                    t.join() # make sure conversion completes
                    messagebox.showinfo("Success!", "Conversion successful!")
            except queue.Empty:
                self.root.after(100, after_callback)
        
        def convert_kismet_to_kml():
            self.view.btn_convert.config(state="disabled") # Disable the Convert button while we do work
            q.put(f"Beginning conversion...")
            input_db = self.view.ent_input_browse.get()
            packets = self.model.get_packets_from_db(input_db)
            devices = self.model.get_devices_from_db(input_db)
            heatworm = self.view.v_heatworm.get()
            q.put(f"Processing {len(packets)} packets and {len(devices)} devices...")
            kml = self.model.build_kml(packets, devices, heatworm)
            q.put("Writing file...")
            output_file = self.view.ent_output_browse.get()
            if self.view.v_compress_kml.get():
                kml.savekmz(output_file, False)
            else:
                kml.save(output_file, False)
            q.put(f"All done!")
            self.view.btn_convert.config(state="normal") # Enable Convert button now that we're done!
            q.put(None)

        try:
            if not self.view.ent_input_browse.get():
                raise ValueError("Missing input file.")
            elif not self.view.ent_output_browse.get():
                raise ValueError("Missing output file.")
            else:
                t = Thread(target=convert_kismet_to_kml)
                t.start()
                self.root.after(100, after_callback)
        except ValueError as e:
            messagebox.showerror("Error!", f"Failed to start conversion: {e}")
        finally:
            return "break"