#Author:Vishal Oshada Sudasingha
#Date: 22/12/2024



import tkinter as tk
from tkinter import ttk
import _tkinter


def is_leap_year(year): # Function to check if the given year is a leap year.
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def validate_date_input(): # Function to validate the user's date input.
    while True:
        try:
            date = int(
                input("Please enter the day of the survey in the format dd: ")) # Prompt the user to enter a date.
            if not 1 <= date <= 31: # Check if the day is in the 1-31 range.
                print("Out of range - values must be in the range 1 and 31.") # Error message for invalid range.
                continue # Restart the loop.
        except ValueError: # Handle non integer input.
            print("Integer required.") # Error message for invalid data type.
            continue  # Restart the loop.
        break # Exit the loop when the valid day is entered.

    while True:
        try:
            month = int(
                input("Please enter the month of the survey in the format MM: ")) # Prompt the user to enter a month.
            if not 1 <= month <= 12: # Check if the month is in the 1-12 range.
                print("Out of range - values must be in the range 1 and 12.") # Error message for invalid range.
                continue # Restart the loop.
        except ValueError:  # Handle non integer input.
            print("Integer required.") # Error message for invalid data type.
            continue # Restart the loop.
        break # Exit the loop when the valid day is entered.

    while True:
        try:
            year = int(
                input("Please enter the year of the survey in the format YYYY: ")) # Prompt the user to enter a year.
            if not 2000 <= year <= 2024: # Check if the year is in the 2000-2024 range.
                print("Out of range - values must be in the range 2000 and 2024.") # Error message for invalid range.
                continue # Restart the loop.
        except ValueError: # Handle non integer input.
            print("Integer required.") # Error message for invalid data type.
            continue # Restart the loop.
        break # Exit the loop when the valid day is entered.

    # Determine the maximum number of days allowed for the entered month and year.
    if month in [1, 3, 5, 7, 8, 10, 12]: # Months with 31 days.
        max_days = 31
    elif month in [4, 6, 9, 11]: # Months with 30 days.
        max_days = 30
    elif month == 2: # Special case: February.
        max_days = 29 if is_leap_year(year) else 28 # Leap year check using is_leap_year function.

    if not 1 <= date <= max_days: # Validate if the entered day is within the range for the determined max_days.
        print(f"Invalid day for the given month and year. Re-enter the date.")
        return validate_date_input() #Restart the process if the day is invalid

    return date, month, year


class HistogramApp: # Initializes the HistogramApp class.
    def __init__(self, traffic_data, date):
        self.traffic_data = traffic_data # Store the traffic data
        self.date = date  # Store the date
        self.root = tk.Tk()  # Initialize the Tkinter root window
        self.canvas = None  # Placeholder for the canvas widget

    def setup_window(self): # Sets up the main application window and canvas.
        self.root.title(f"Histogram - {self.date}") # Set the title of the window with the provided date.
        self.canvas = tk.Canvas(self.root, width=3300, height=900, bg="#e6e2df")
        self.canvas.pack() # Pack the canvas to make it visible

    def draw_histogram(self): # Draws a histogram based on traffic data, showing vehicle frequency for two junctions:
        # Elm and Hanley.

        hourly_counts = {'Elm': {}, 'Hanley': {}} # Dictionary to store hourly vehicle counts for both junctions.

        # Initialize hourly counts for each junction.
        for row in self.traffic_data:
            hour = row['timeOfDay'][:2]  # Extract the hour from the time string (e.g., "08:00" -> "08").
            junction = 'Elm' if 'Elm' in row['JunctionName'] else 'Hanley' # Initialize hourly count if the hour is not
            # already present.
            if hour not in hourly_counts[junction]:
                hourly_counts[junction][hour] = 0
            hourly_counts[junction][hour] += 1 # Increment the count for the corresponding hour and junction.

        # Calculate the maximum count for scaling the histogram
        max_count = max(
            max(hourly_counts['Elm'].values(), default=0), # Max count for Elm junction.
            max(hourly_counts['Hanley'].values(), default=0) # Max count for Hanley highway.
        )
        # Set the dimensions and positions for the bars in the histogram.
        bar_width = 20 # Width of each bar.
        spacing = 0 # Space between bars within a group.
        group_spacing = 9 # Space between groups of bars.
        x_offset = 70 # Starting position for the X-axis.
        y_offset = 550 # Starting position for the Y-axis.

        # Draw axes.
        # Create the line.
        self.canvas.create_line(x_offset, y_offset, x_offset + 1150, y_offset, fill="black", width=2)

        # Add the text to the line.
        self.canvas.create_text(x_offset + 500, y_offset + 60, text="Hours 00:00 to 24:00", fill="black",
                                font=("Arial", 12))

        hours = sorted(set(hourly_counts['Elm'].keys()).union(set(hourly_counts['Hanley'].keys())))
        for i, hour in enumerate(hours):
            # Calculate positions for Elm and Hanley bars.
            x_group_start = x_offset + i * (2 * bar_width + group_spacing)
            x_elm = x_group_start
            x_hanley = x_group_start + bar_width + spacing

            # Heights of the bars.
            elm_count = hourly_counts['Elm'].get(hour, 0)
            hanley_count = hourly_counts['Hanley'].get(hour, 0)
            elm_height = int((elm_count / max_count) * 300) if max_count > 0 else 0
            hanley_height = int((hanley_count / max_count) * 300) if max_count > 0 else 0

            # Draw Elm bar and count label.
            self.canvas.create_rectangle(
                x_elm, y_offset - elm_height, x_elm + bar_width, y_offset,
                fill="#0b0270"
            )
            self.canvas.create_text(
                x_elm + bar_width / 2, y_offset - elm_height - 10,
                text=str(elm_count), font=("Arial", 8)
            )

            # Draw Hanley bar and count label.
            self.canvas.create_rectangle(
                x_hanley, y_offset - hanley_height, x_hanley + bar_width, y_offset,
                fill="#ebf705"
            )
            self.canvas.create_text(
                x_hanley + bar_width / 2, y_offset - hanley_height - 10,
                text=str(hanley_count), font=("Arial", 8)
            )

            # Add the hour label below the group of bars.
            self.canvas.create_text(
                (x_elm + x_hanley + bar_width) / 2, y_offset + 20,
                text=f"{hour}", font=("Arial", 10)
            )

        # Add the title for the histogram.
        self.canvas.create_text(350, 20, text=f"Histogram of Vehicle Frequency per Hour ({self.date}) ",
                                font=("Arial", 16, "bold"))

    # Add a legend to describe the histogram colours.
    def add_legend(self):
        self.canvas.create_rectangle(90, 80, 110, 100, fill="#0b0270") # Rectangle for Elm.
        self.canvas.create_text(120, 90, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))

        self.canvas.create_rectangle(90, 110, 110, 130, fill="#ebf705") # Rectangle for Hanley
        self.canvas.create_text(120, 120, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10))

    def run(self): # Sets up the application and starts the main event loop.
        self.setup_window()  # Initialize the window.
        self.draw_histogram() # Draw the histogram.
        self.add_legend() # Add the legend.
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy) # Handle window close.
        self.root.mainloop() #  Start the Tkinter event loop.


class MultiCSVProcessor: # Handles loading and processing of multiple CSV files containing traffic data.
    def __init__(self):
        self.current_data = [] # Store the currently loaded traffic data.

    def load_csv_file(self, date, month, year): # Loads traffic data from a CSV file based on the provided date.
        file_name = f"traffic_data{date:02d}{month:02d}{year}.csv" # Format the file name.
        try:
            with open(file_name, 'r') as file:
                self.current_data = []
                header = file.readline().strip().split(',') # Read the header.
                for line in file:
                    values = line.strip().split(',')
                    row = {header[i]: values[i] for i in range(len(header))} # Map header to values.
                    self.current_data.append(row)
            print(f"Loaded {file_name} successfully.")
        except FileNotFoundError:
            print(f"File {file_name} not found.")

    def handle_user_interaction(self): # Manages user interaction for selecting CSV files and viewing histograms.
        while True:
            date, month, year = validate_date_input() # Get date input.
            self.load_csv_file(date, month, year) # Load the corresponding CSV file.
            app = HistogramApp(self.current_data, f"{date:02d}/{month:02d}/{year}") # Run the histogram app.
            app.run()
            user_input = input("Do you want to select another data file for a different date? (Y/N): ").strip().lower()
            if user_input != "y":
                print("Existing the application.")
                break


def main(): # Main function to run the application..
    print("___Welcome to the H.O.V.F APP 2024___")
    processor = MultiCSVProcessor() # Initialize the CSV processor.
    app = None # Variable to hold the current app instance.
    while True:
        date, month, year = validate_date_input() # Get date input.
        processor.load_csv_file(date, month, year) # Load the data

        if app:
            try:
                if app.root and app.root.winfo_exists():
                        app.root.destroy() # Close the existing app window.
            except _tkinter.TclError:
                pass

        app = HistogramApp(processor.current_data, f"{date:02d}/{month:02d}/{year}") # Create a new app instance.

        app.setup_window() # Set up the window.
        app.draw_histogram() # Draw the histogram.
        app.add_legend() # Add the legend.

        def on_user_input():
            user_input = input("Do you want to select another data file for a different date? (Y/N): ").strip().lower()
            if user_input == 'y':
                if app.root.winfo_exists():
                    app.root.destroy() # Destroy the current window.

            else:
                print("Thank you!exiting the application.")
                if app.root.winfo_exists():
                    app.root.destroy() # Ensure window is closed.
                exit()  # Terminate the program.

        app.root.after(100, on_user_input) # Handle user input after the app starts.
        app.root.mainloop() # Start the main loop.



if __name__ == "__main__":
    main() # Run the program.
# if you have been contracted to do this assignment please do not remove this line.
