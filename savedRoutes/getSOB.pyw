import os
import configparser

# Define the planets with initial scores (these will be updated)
planets = {
    "aquas": 0,
    "area 6": 0,
    "bolse": 0,
    "corneria": 0,
    "fortuna": 0,
    "katina": 0,
    "macbeth": 0,
    "meteo": 0,
    "sector x": 0,
    "sector y": 0,
    "sector z": 0,
    "solar": 0,
    "titania": 0,
    "venom 1": 0,
    "venom 2": 0,
    "zoness": 0,
    "total": 0
}

def load_existing_scores(folder_path):
    # Initialize the existing scores dictionary
    existing_scores = {planet: 0 for planet in planets}

    sum_of_best_path = os.path.join(folder_path, 'Sum_Of_Best.ini')
    
    if os.path.exists(sum_of_best_path):
        config = configparser.ConfigParser()
        config.read(sum_of_best_path)
        
        if 'Sum_Of_Best' in config:
            for planet in planets:
                if planet in config['Sum_Of_Best']:
                    try:
                        existing_scores[planet] = int(config['Sum_Of_Best'][planet])
                    except ValueError:
                        pass
    
    return existing_scores

def scan_ini_files(folder_path, existing_scores):
    # Initialize the best scores dictionary with existing scores
    best_scores = {planet: existing_scores[planet] for planet in planets}

    # List all .ini files in the folder_path
    for filename in os.listdir(folder_path):
        # Skip the Sum_Of_Best.ini file
        if filename.endswith(".ini") and filename != "Sum_Of_Best.ini":
            file_path = os.path.join(folder_path, filename)
            print(f"Checking INI file path: {file_path}")

            # Parse the .ini file
            config = configparser.ConfigParser()
            config.read(file_path)
            
            # Scan through sections in the .ini file
            for section in config.sections():
                for planet in best_scores:
                    if planet in config[section]:
                        try:
                            score = int(config[section][planet])
                            # Update the best score if the current one is higher
                            if score > best_scores[planet]:
                                best_scores[planet] = score
                        except ValueError:
                            # Skip non-integer values
                            pass

    # Calculate total score
    best_scores["total"] = sum(best_scores[planet] for planet in planets if planet != "total")
    
    return best_scores

def save_to_ini_file(best_scores, folder_path):
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    
    # Add a section and populate it with the best scores
    config.add_section('Sum_Of_Best')
    for planet, score in best_scores.items():
        config.set('Sum_Of_Best', planet, str(score))
    
    # Write the configuration to an .ini file
    sum_of_best_path = os.path.join(folder_path, 'Sum_Of_Best.ini')
    with open(sum_of_best_path, 'w') as configfile:
        config.write(configfile)
    print(f"Saved Sum Of Best to: {sum_of_best_path}")

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the folder path relative to this script's directory
    folder_path = script_dir
    print(f"Current working directory in getSOB: {folder_path}")

    # Ensure folder_path exists before scanning
    if not os.path.exists(folder_path):
        print(f"Folder path does not exist: {folder_path}")
        return

    existing_scores = load_existing_scores(folder_path)
    best_scores = scan_ini_files(folder_path, existing_scores)
    save_to_ini_file(best_scores, folder_path)
    
    # Print the best scores for each planet
    for planet, score in best_scores.items():
        print(f"{planet}: {score}")

if __name__ == "__main__":
    main()
