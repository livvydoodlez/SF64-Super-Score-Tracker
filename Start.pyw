from tkinter import *
from tkinter import ttk, messagebox
from config.variables import *
from config.settings import *
import configparser
import os

# Load color settings from settings.ini if available
config = configparser.ConfigParser()
config.read('config/settings.ini')

color_settings.update({
    'font_size': config.get('COLOR_SETTINGS', 'font_size'),
    'font_color_hex': config.get('COLOR_SETTINGS', 'font_color_hex'),
    'background_color_hex': config.get('COLOR_SETTINGS', 'background_color_hex'),
    'button_font_size': config.get('COLOR_SETTINGS', 'button_font_size'),
    'button_font_color_hex': config.get('COLOR_SETTINGS', 'button_font_color_hex'),
    'button_bg_color_hex': config.get('COLOR_SETTINGS', 'button_bg_color_hex'),
})



last_selected_route = None
if 'LAST_SELECTED_ROUTE' in config:
    last_selected_route = config['LAST_SELECTED_ROUTE'].get('route_name', None)


if 'COLOR_SETTINGS' in config:
    color_settings.update(config['COLOR_SETTINGS'])

# Create savedRoutes folder if it doesn't exist
if not os.path.exists('savedRoutes'):
    os.makedirs('savedRoutes')

class ScoreTracker:
    def __init__(self):
        self.root = Tk()
        self.root.title("SF64 Super Score Tracker")
        self.root.minsize(453, 453)  # Set minimum window size
        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg=color_settings['background_color_hex'])

        # Frame for route selection
        frame_routes = Frame(self.root, bg=color_settings['background_color_hex'])
        frame_routes.pack(fill='x', padx=10, pady=10)

        Label(frame_routes, text="Select Route:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).pack(side='left', padx=(0, 10))

        self.clicked = StringVar()
        default_route = list(route_to_planets.keys())[0] if last_selected_route is None else last_selected_route
        self.clicked.set(default_route)  # Set default route

        # Create a list of display names for OptionMenu (with numbers)
        route_display_names = [f"{i+1}. {route}" for i, route in enumerate(route_to_planets.keys())]

        self.drop = OptionMenu(frame_routes, self.clicked, *route_display_names, command=self.update_label)
        self.drop.configure(bg=color_settings['dropdown_bg_color_hex'], fg=color_settings['font_color_hex'], bd=1,
                            activebackground=color_settings['dropdown_bg_color_hex'],
                            activeforeground=color_settings['font_color_hex'])
        self.drop['menu'].configure(bg=color_settings['dropdown_bg_color_hex'], fg=color_settings['font_color_hex'])
        self.drop.pack(side='left', fill='x', expand=True)

        # Display selected route dynamically (without the number)
        self.label_selected_route = Label(self.root, text=f"Selected Route: {self.clicked.get().split('. ', 1)[-1]}",
                                          bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                                          font=("Arial", int(color_settings['font_size'])))
        self.label_selected_route.pack(anchor='w', padx=10, pady=(0, 10))

        # Frame for planet data
        self.frame_planets = Frame(self.root, bg=color_settings['background_color_hex'])
        self.frame_planets.pack(fill='both', expand=True, padx=10)

        # Initialize current and best scores based on selected route
        selected_route_name = self.clicked.get().split('. ', 1)[-1]  # Extract route name without number prefix
        self.current_scores = [0] * len(route_to_planets[selected_route_name])
        self.best_scores = [0] * len(route_to_planets[selected_route_name])
        self.load_saved_route()

        self.display_planet_data(selected_route_name)  # Update UI with selected route name only

        # Label for "Made by: Livvydoodlez"
        Label(self.root, text="Made by: Livvydoodlez", bg=color_settings['background_color_hex'],
              fg=color_settings['font_color_hex'], font=("Arial", int(color_settings['font_size']))).pack(anchor='w', padx=10, pady=(20, 10))

        # Frame for buttons
        frame_buttons = Frame(self.root, bg=color_settings['background_color_hex'])
        frame_buttons.pack(fill='x', padx=10, pady=(10, 0))

        Button(frame_buttons, text="Save Route", width=20, font=("Arial", int(color_settings['button_font_size'])),
               bg=color_settings['button_bg_color_hex'], fg=color_settings['button_font_color_hex'],
               command=self.save_route_popup).pack(pady=5, fill='x')
        Button(frame_buttons, text="Settings", width=20, font=("Arial", int(color_settings['button_font_size'])),
               bg=color_settings['button_bg_color_hex'], fg=color_settings['button_font_color_hex'],
               command=self.open_settings_window).pack(pady=5, fill='x')

        # Bind window resize event
        self.root.bind('<Configure>', lambda event, frame=self.frame_planets: self.on_window_resize(event, frame))

        # Pack the main window
        self.root.mainloop()




    def load_saved_route(self):
        print("Attempting to load saved route...")  # Debugging statement

        selected_route_name = self.clicked.get()  # Get the selected route name directly
        route_name = selected_route_name.split('. ', 1)[-1]  # Extract route name without the number prefix
        ini_file = os.path.join('savedRoutes', f'{route_name}.ini')

        print(f"Selected route: {selected_route_name}")
        print(f"Route name: {route_name}")
        print(f"Checking INI file path: {ini_file}")  # Debugging statement

        if os.path.exists(ini_file):
            config = configparser.ConfigParser()
            config.read(ini_file)

            if route_name in config:
                self.best_scores = []
                planets = route_to_planets[route_name]

                for planet in planets:
                    if planet in config[route_name]:
                        try:
                            best_score = int(config[route_name][planet])
                        except ValueError:
                            best_score = 0
                        self.best_scores.append(best_score)
                    else:
                        self.best_scores.append(0)

                self.display_planet_data(route_name)
        else:
            self.best_scores = [0] * len(route_to_planets[route_name])
            self.display_planet_data(route_name)


        

    def save_route_popup(self):
        confirm = messagebox.askquestion("Confirm Save", "Are you sure you want to save the route?")
        if confirm == 'yes':
            self.save_route()

    def save_route(self):
        route_name = self.clicked.get()
        updated = False  # Flag to track if any score was updated

        # Update best scores if current scores are higher
        for i, planet in enumerate(route_to_planets[route_name]):
            current_score = self.current_scores[i]
            if current_score > self.best_scores[i]:
                self.best_scores[i] = current_score
                updated = True  # Set flag if any score is updated

        # Save route data to INI file only if there's an actual improvement
        if updated:
            config = configparser.ConfigParser()
            config[route_name] = {}

            # Iterate through planets and add scores to config
            planets = route_to_planets[route_name]
            for i, planet in enumerate(planets):
                if planet != "Total":
                    config[route_name][planet] = str(self.best_scores[i])  # Always save the best score

            # Calculate and add total score to config
            total_score = sum(self.current_scores)
            config[route_name]["Total"] = str(total_score)

            with open(f'savedRoutes/{route_name}.ini', 'w') as configfile:
                config.write(configfile)

            # Save last selected route to settings.ini
            if 'LAST_SELECTED_ROUTE' not in config:
                config['LAST_SELECTED_ROUTE'] = {}
            config['LAST_SELECTED_ROUTE']['route_name'] = route_name

            # Preserve the COLOR_SETTINGS section
            if color_settings:
                config['COLOR_SETTINGS'] = color_settings

            # Write the updated config back to the file
            with open('config/settings.ini', 'w') as configfile:
                config.write(configfile)

            # Re-create the widgets to reflect the updated data
            self.load_saved_route()
        else:
            messagebox.showinfo("No Improvement", "No improvements to save. Current scores are not better than existing best scores.")




    def update_label(self, selected_route):
        # Extract the route name without the number prefix
        selected_route_name = selected_route.split('. ', 1)[-1]
        self.clicked.set(selected_route_name)  # Set the full selected route name
        self.load_saved_route()
        self.label_selected_route.config(text=f"Selected Route: {selected_route_name}")

        # Update current scores and display data for the selected route
        self.current_scores = [0] * len(route_to_planets[selected_route_name])
        self.display_planet_data(selected_route_name)



    def display_planet_data(self, selected_route):
        selected_route_name = self.clicked.get()  # Get the selected route name directly
        planets = route_to_planets[selected_route_name]
        # Clear existing widgets in frame_planets
        for widget in self.frame_planets.winfo_children():
            widget.destroy()

        # Get the list of planet names for the selected route
        planets = route_to_planets.get(selected_route, [])

        # Display planet names dynamically
        Label(self.frame_planets, text="Planet:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=0, column=0, sticky='w')
        Label(self.frame_planets, text="Current Score:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=0, column=3, sticky='e')
        Label(self.frame_planets, text="Best Score:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=0, column=6, sticky='e')
        Label(self.frame_planets, text="Difference:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=0, column=7, sticky='e')

        # Dictionary to hold current scores
        self.current_scores_dict = {}

        for i, planet in enumerate(planets, start=1):
            Label(self.frame_planets, text=f"{planet}:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                  font=("Arial", int(color_settings['font_size'])), anchor='w').grid(row=i, column=0, padx=10, pady=5)
            
            # Create Entry widget for current score
            if planet != "Current Score":
                entry = Entry(self.frame_planets, width=5, validate="key", validatecommand=(self.root.register(self.on_entry_update(i-1, planets)), '%P'))
                entry.grid(row=i, column=5, sticky='e', padx=(0, 1), pady=5)
                self.frame_planets.grid_columnconfigure(3, weight=1, minsize=50)  # Adjust column width

            # Get best score for the planet (replace with actual logic to retrieve best score)
            best_score = self.best_scores[i-1]

            # Initialize current score
            current_score = self.current_scores[i-1]
            self.current_scores_dict[planet] = current_score

            # Calculate initial difference
            difference = current_score - best_score

            # Display current score
            """Label(self.frame_planets, text=str(current_score), bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                  font=("Arial", int(color_settings['font_size']))).grid(row=i, column=3, sticky='e', padx=(0, 10), pady=5)"""
            
            # Display best score
            Label(self.frame_planets, text=str(best_score), bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                  font=("Arial", int(color_settings['font_size']))).grid(row=i, column=6, sticky='e', padx=(0, 10), pady=5)
            
            # Display difference with color coding
            difference_label = Label(self.frame_planets, text=str(difference), bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                                     font=("Arial", int(color_settings['font_size'])))
            difference_label.grid(row=i, column=7, sticky='e', padx=(0, 10), pady=5)

            # Apply color coding based on difference
            if difference < 0:
                difference_label.config(fg=color_settings['worst_than_pb_color_hex'])
            elif difference == 0:
                difference_label.config(fg=color_settings['same_as_pb_color_hex'])
            else:
                difference_label.config(fg=color_settings['new_pb_color_hex'])

        # Calculate total score and its difference from best score
        total_score = sum(self.current_scores)
        total_best_score = sum(self.best_scores)
        total_difference = total_score - total_best_score

        # Display total row
        Label(self.frame_planets, text="Total:", bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=len(planets) + 1, column=0, sticky='w')
        Label(self.frame_planets, text=str(total_score), bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=len(planets) + 1, column=3, sticky='e')
        Label(self.frame_planets, text=str(total_best_score), bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
              font=("Arial", int(color_settings['font_size']))).grid(row=len(planets) + 1, column=6, sticky='e')
        total_difference_label = Label(self.frame_planets, text=str(total_difference), bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                                       font=("Arial", int(color_settings['font_size'])))
        total_difference_label.grid(row=len(planets) + 1, column=7, sticky='e', padx=(0, 10), pady=5)

        # Apply color coding for total difference
        if total_difference < 0:
            total_difference_label.config(fg=color_settings['worst_than_pb_color_hex'])
        elif total_difference == 0:
            total_difference_label.config(fg=color_settings['same_as_pb_color_hex'])
        else:
            total_difference_label.config(fg=color_settings['new_pb_color_hex'])

    def on_entry_update(self, index, planets):
        def callback(value):
            if value == "":
                self.current_scores[index] = 0  # Handle empty string as 0
            elif value.isdigit() or (value == "-" and len(value) == 1):
                self.current_scores[index] = int(value)

            # Update difference labels dynamically
            for i, planet in enumerate(route_to_planets[self.clicked.get()]):
                current_score = self.current_scores[i]
                best_score = self.best_scores[i]
                difference = current_score - best_score

                # Find the difference label widget and update its text
                for child in self.frame_planets.winfo_children():
                    if child.grid_info()['row'] == i + 1 and child.grid_info()['column'] == 7:
                        child.config(text=str(difference))

                        # Apply color coding based on difference
                        if difference < 0:
                            child.config(fg=color_settings['worst_than_pb_color_hex'])
                        elif difference == 0:
                            child.config(fg=color_settings['same_as_pb_color_hex'])
                        else:
                            child.config(fg=color_settings['new_pb_color_hex'])

            # Update total score and its difference from best score
            total_score = sum(self.current_scores)
            total_best_score = sum(self.best_scores)
            total_difference = total_score - total_best_score

            # Find the total difference label widget and update its text
            for child in self.frame_planets.winfo_children():
                if child.grid_info()['row'] == len(planets) + 1 and child.grid_info()['column'] == 7:
                    child.config(text=str(total_difference))

                    # Apply color coding based on total difference
                    if total_difference < 0:
                        child.config(fg=color_settings['worst_than_pb_color_hex'])
                    elif total_difference == 0:
                        child.config(fg=color_settings['same_as_pb_color_hex'])
                    else:
                        child.config(fg=color_settings['new_pb_color_hex'])

            self.update_total_score()
            return True

        return callback

    def update_total_score(self):
        total_score = sum(self.current_scores)
        # Update total score label
        for widget in self.frame_planets.winfo_children():
            if widget.grid_info()['row'] == len(route_to_planets[self.clicked.get()]) + 1 and \
                    widget.grid_info()['column'] == 3:
                widget.config(text=str(total_score))

    def on_window_resize(self, event, parent_frame):
        # Adjust the width of planet labels and entries when the window is resized
        for widget in parent_frame.winfo_children():
            widget.grid_configure(sticky='we')


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
            font_color_entry = Entry(self.settings_window, width=20)
            font_color_entry.grid(row=1, column=1, padx=10, pady=5)
            font_color_entry.insert(0, color_settings['font_color_hex'])

            Label(self.settings_window, text="Background Color (Hex):", anchor='w').grid(row=2, column=0, padx=10, pady=5)
            background_color_entry = Entry(self.settings_window, width=20)
            background_color_entry.grid(row=2, column=1, padx=10, pady=5)
            background_color_entry.insert(0, color_settings['background_color_hex'])

            Label(self.settings_window, text="Dropdown BG Color (Hex):", anchor='w').grid(row=3, column=0, padx=10, pady=5)
            dropdown_bg_color_entry = Entry(self.settings_window, width=20)
            dropdown_bg_color_entry.grid(row=3, column=1, padx=10, pady=5)
            dropdown_bg_color_entry.insert(0, color_settings['dropdown_bg_color_hex'])

            Label(self.settings_window, text="Dropdown Border Color (Hex):", anchor='w').grid(row=4, column=0, padx=10, pady=5)
            dropdown_border_color_entry = Entry(self.settings_window, width=20)
            dropdown_border_color_entry.grid(row=4, column=1, padx=10, pady=5)
            dropdown_border_color_entry.insert(0, color_settings['dropdown_border_color_hex'])

            Label(self.settings_window, text="Button Font Size:", anchor='w').grid(row=5, column=0, padx=10, pady=5)
            button_font_size_entry = Entry(self.settings_window, width=10)
            button_font_size_entry.grid(row=5, column=1, padx=10, pady=5)
            button_font_size_entry.insert(0, color_settings['button_font_size'])

            Label(self.settings_window, text="Button Font Color (Hex):", anchor='w').grid(row=6, column=0, padx=10, pady=5)
            button_font_color_entry = Entry(self.settings_window, width=20)
            button_font_color_entry.grid(row=6, column=1, padx=10, pady=5)
            button_font_color_entry.insert(0, color_settings['button_font_color_hex'])

            Label(self.settings_window, text="Button Background Color (Hex):", anchor='w').grid(row=7, column=0, padx=10, pady=5)
            button_bg_color_entry = Entry(self.settings_window, width=20)
            button_bg_color_entry.grid(row=7, column=1, padx=10, pady=5)
            button_bg_color_entry.insert(0, color_settings['button_bg_color_hex'])

            Label(self.settings_window, text="Worse Than PB Color (Hex):", anchor='w').grid(row=8, column=0, padx=10, pady=5)
            worst_than_pb_color_entry = Entry(self.settings_window, width=20)
            worst_than_pb_color_entry.grid(row=8, column=1, padx=10, pady=5)
            worst_than_pb_color_entry.insert(0, color_settings['worst_than_pb_color_hex'])

            Label(self.settings_window, text="Same As PB Color (Hex):", anchor='w').grid(row=9, column=0, padx=10, pady=5)
            same_as_pb_color_entry = Entry(self.settings_window, width=20)
            same_as_pb_color_entry.grid(row=9, column=1, padx=10, pady=5)
            same_as_pb_color_entry.insert(0, color_settings['same_as_pb_color_hex'])

            Label(self.settings_window, text="New PB Color (Hex):", anchor='w').grid(row=10, column=0, padx=10, pady=5)
            new_pb_color_entry = Entry(self.settings_window, width=20)
            new_pb_color_entry.grid(row=10, column=1, padx=10, pady=5)
            new_pb_color_entry.insert(0, color_settings['new_pb_color_hex'])

            warning_label = Label(self.settings_window, text="Color settings are in (RRGGBB) Format (Fuck python)", anchor='center')
            warning_label.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')


            warning_label = Label(self.settings_window, text="WARNING! SETTINGS WILL ONLY APPLY NORMALLY AFTER RESTARTING PROGRAM!", anchor='center')
            warning_label.grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')


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
                new_pb_color_entry.get()
            )).grid(row=13, column=0, columnspan=2, pady=10)

    def save_settings(self, font_size, font_color_hex, background_color_hex, dropdown_bg_color_hex, dropdown_border_color_hex, button_font_size, button_font_color_hex, button_bg_color_hex, worst_than_pb_color_hex, same_as_pb_color_hex, new_pb_color_hex):
        # Update color settings dictionary
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

        # Save settings back to the .ini file
        config.set('COLOR_SETTINGS', 'font_size', font_size)
        config.set('COLOR_SETTINGS', 'font_color_hex', font_color_hex)
        config.set('COLOR_SETTINGS', 'background_color_hex', background_color_hex)
        config.set('COLOR_SETTINGS', 'dropdown_bg_color_hex', dropdown_bg_color_hex)
        config.set('COLOR_SETTINGS', 'dropdown_border_color_hex', dropdown_border_color_hex)
        config.set('COLOR_SETTINGS', 'button_font_size', button_font_size)
        config.set('COLOR_SETTINGS', 'button_font_color_hex', button_font_color_hex)
        config.set('COLOR_SETTINGS', 'button_bg_color_hex', button_bg_color_hex)
        config.set('COLOR_SETTINGS', 'worst_than_pb_color_hex', worst_than_pb_color_hex)
        config.set('COLOR_SETTINGS', 'same_as_pb_color_hex', same_as_pb_color_hex)
        config.set('COLOR_SETTINGS', 'new_pb_color_hex', new_pb_color_hex)

        with open('path_to_your_config_file.ini', 'w') as configfile:
            config.write(configfile)

        # Reload settings from the .ini file
        config.read('path_to_your_config_file.ini')
        color_settings.update(config['COLOR_SETTINGS'])

        # Write color settings to settings.ini
        config['COLOR_SETTINGS'] = color_settings
        with open('config/settings.ini', 'w') as configfile:
            config.write(configfile)

        # Update GUI elements with new color settings
        self.root.configure(bg=color_settings['background_color_hex'])
        self.label_selected_route.config(bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                                         font=("Arial", int(color_settings['font_size'])))
        for widget in self.frame_planets.winfo_children():
            widget.configure(bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                             font=("Arial", int(color_settings['font_size'])))
        for child in self.frame_planets.winfo_children():
            child.configure(bg=color_settings['background_color_hex'], fg=color_settings['font_color_hex'],
                            font=("Arial", int(color_settings['font_size'])))
        self.settings_window.destroy()
        self.settings_window = None

    def close_settings_window(self):
        self.settings_window.destroy()
        self.settings_window = None



if __name__ == "__main__":
    ScoreTracker()
