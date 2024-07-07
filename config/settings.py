def open_settings_window(self):
    if not hasattr(self, 'settings_window') or self.settings_window is None:
        self.settings_window = Toplevel(self.root)
        self.settings_window.title("Color Settings")
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings_window)  # Handle window close event

        # Create and pack widgets for color settings
        Label(self.settings_window, text="Font Size:", anchor='w').grid(row=0, column=0, padx=10, pady=5)
        font_size_entry = Entry(self.settings_window, width=10)
        font_size_entry.grid(row=0, column=1, padx=10, pady=5)
        font_size_entry.insert(0, color_settings['font_size'])

        Label(self.settings_window, text="Font Color (Hex):", anchor='w').grid(row=1, column=0, padx=10, pady=5)
        font_color_entry = Entry(self.settings_window, width=10)
        font_color_entry.grid(row=1, column=1, padx=10, pady=5)
        font_color_entry.insert(0, color_settings['font_color_hex'])

        Label(self.settings_window, text="Background Color (Hex):", anchor='w').grid(row=2, column=0, padx=10, pady=5)
        background_color_entry = Entry(self.settings_window, width=10)
        background_color_entry.grid(row=2, column=1, padx=10, pady=5)
        background_color_entry.insert(0, color_settings['background_color_hex'])

        Label(self.settings_window, text="Drop Down BG Color (Hex):", anchor='w').grid(row=3, column=0, padx=10, pady=5)
        dropdown_bg_color_entry = Entry(self.settings_window, width=10)
        dropdown_bg_color_entry.grid(row=3, column=1, padx=10, pady=5)
        dropdown_bg_color_entry.insert(0, color_settings['dropdown_bg_color_hex'])

        Label(self.settings_window, text="Drop Down Border Color (Hex):", anchor='w').grid(row=4, column=0, padx=10, pady=5)
        dropdown_border_color_entry = Entry(self.settings_window, width=10)
        dropdown_border_color_entry.grid(row=4, column=1, padx=10, pady=5)
        dropdown_border_color_entry.insert(0, color_settings['dropdown_border_color_hex'])

        Label(self.settings_window, text="Button Font Size:", anchor='w').grid(row=5, column=0, padx=10, pady=5)
        button_font_size_entry = Entry(self.settings_window, width=10)
        button_font_size_entry.grid(row=5, column=1, padx=10, pady=5)
        button_font_size_entry.insert(0, color_settings['button_font_size'])

        Label(self.settings_window, text="Button Font Color (Hex):", anchor='w').grid(row=6, column=0, padx=10, pady=5)
        button_font_color_entry = Entry(self.settings_window, width=10)
        button_font_color_entry.grid(row=6, column=1, padx=10, pady=5)
        button_font_color_entry.insert(0, color_settings['button_font_color_hex'])

        Label(self.settings_window, text="Button Background Color (Hex):", anchor='w').grid(row=7, column=0, padx=10, pady=5)
        button_bg_color_entry = Entry(self.settings_window, width=10)
        button_bg_color_entry.grid(row=7, column=1, padx=10, pady=5)
        button_bg_color_entry.insert(0, color_settings['button_bg_color_hex'])

        Label(self.settings_window, text="Worst Thank PB Color (Hex):", anchor='w').grid(row=8, column=0, padx=10, pady=5)
        worst_than_pb_color_entry = Entry(self.settings_window, width=10)
        worst_than_pb_color_entry.grid(row=8, column=1, padx=10, pady=5)
        worst_than_pb_color_entry.insert(0, color_settings['worst_than_pb_color_hex'])

        Label(self.settings_window, text="Same As PB Color (Hex):", anchor='w').grid(row=9, column=0, padx=10, pady=5)
        same_as_pb_color_entry = Entry(self.settings_window, width=10)
        same_as_pb_color_entry.grid(row=9, column=1, padx=10, pady=5)
        same_as_pb_color_entry.insert(0, color_settings['same_as_pb_color_hex'])

        Label(self.settings_window, text="New PB Color (Hex):", anchor='w').grid(row=10, column=0, padx=10, pady=5)
        new_pb_color_entry = Entry(self.settings_window, width=10)
        new_pb_color_entry.grid(row=10, column=1, padx=10, pady=5)
        new_pb_color_entry.insert(0, color_settings['new_pb_color_hex'])

        # Save button
        Button(self.settings_window, text="Save", command=lambda: self.save_settings(
            font_size_entry.get(),
            font_color_entry.get(),
            background_color_entry.get(),
            dropdown_bg_color_entry.get(),
            dropdown_border_color_entry.get(),
            button_font_size_entry.get(),
            button_font_color_entry.get(),
            button_bg_color_entry.get(),
            worst_than_pb_color_entry.get(),
            same_as_pb_color_entry.get(),
            new_pb_color_entry.get(),
        )).grid(row=11, column=0, columnspan=2, pady=(10, 0))

def save_settings(self, font_size, font_color_hex, background_color_hex, dropdown_bg_color_hex, dropdown_border_color_hex,
                  button_font_size, button_font_color_hex, button_bg_color_hex, worst_than_pb_color_hex,
                  same_as_pb_color_hex, new_pb_color_hex):
    # Update color_settings dictionary
    color_settings.update({
        'font_size': font_size,
        'font_color_hex': font_color_hex,
        'background_color_hex': background_color_hex,
        'dropdown_bg_color_hex': dropdown_bg_color_hex,
        'dropdown_border_color_hex': dropdown_border_color_hex,
        'button_font_size': button_font_size,
        'button_font_color_hex': button_font_color_hex,
        'button_bg_color_hex': button_bg_color_hex,
        'worst_than_pb_color_hex': worst_than_pb_color_hex,
        'same_as_pb_color_hex': same_as_pb_color_hex,
        'new_pb_color_hex': new_pb_color_hex,
    })

    # Save to settings.ini
    config['COLOR_SETTINGS'] = {
        'font_size': font_size,
        'font_color_hex': font_color_hex,
        'background_color_hex': background_color_hex,
        'dropdown_bg_color_hex': dropdown_bg_color_hex,
        'dropdown_border_color_hex': dropdown_border_color_hex,
        'button_font_size': button_font_size,
        'button_font_color_hex': button_font_color_hex,
        'button_bg_color_hex': button_bg_color_hex,
        'worst_than_pb_color_hex': worst_than_pb_color_hex,
        'same_as_pb_color_hex': same_as_pb_color_hex,
        'new_pb_color_hex': new_pb_color_hex,
    }

    with open('config/settings.ini', 'w') as configfile:
        config.write(configfile)

    # Update UI colors
    self.root.configure(bg=background_color_hex)
    for widget in self.root.winfo_children():
        widget.configure(bg=background_color_hex)

    self.label_selected_route.configure(bg=background_color_hex, fg=font_color_hex)
    for entry in self.entry_fields:
        entry.configure(bg=background_color_hex, fg=font_color_hex)

    # Update colors of existing widgets
    for child in self.settings_window.winfo_children():
        child.configure(bg=background_color_hex, fg=font_color_hex)

    # Close the settings window
    self.settings_window.destroy()
    self.settings_window = None

def close_settings_window(self):
    self.settings_window.destroy()
    self.settings_window = None
