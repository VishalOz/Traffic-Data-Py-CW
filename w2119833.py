#Author: Vishal Oshada Sudasingha
#Date: 27/11/2024
#Student ID: 20240036/w2119833

import csv #importing csv module for handle csv files

#Function to check if the given year is a leap year.
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

#Function to validate the user's date input.
def validate_date_input():
    
    while True: #Loop to ensure valid day input.
        try:
            date = int(input("Please enter the day of the survey in the format dd: ")) #Prompt the user to enter a date.
            if not 1 <= date <= 31: #Check if the day is in the 1-31 range.
                print("Out of range - values must be in the range 1 and 31.")#Error message for invalid range.
                continue #Restart the loop.
        except ValueError: #Handle non integer input.
            print("Integer required.") #Error message for invalid data type.
            continue #Restart the loop.
        break #Exit the loop when the valid day is entered.

    while True: #Loop to ensure valid month input.
        try:
            month = int(input("Please enter the month of the survey in the format MM: ")) #Prompt the user to enter a month.
            if not 1 <= month <= 12: #Check if the month is in the 1-12 range.
                print("Out of range - values must be in the range 1 and 12.") #Error message for invalid range.
                continue #Restart the loop
        except ValueError:#Handle non integer input.
            print("Integer required.") #Error message for invalid data type.
            continue #Restart the loop.
        break #Exit the loop when the valid month is entered.

    while True: #Loop to ensure valid month input.
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: ")) #Prompt the user to enter a year.
            if not 2000 <= year <= 2024: #Check if the year is in the 2000-2024 range
                print("Out of range - values must be in the range 2000 and 2024.") #Error message for invalid range.
                continue #Restart the loop.
        except ValueError: #Handle non integer input.
            print("Integer required.") #Error message for invalid data type.
            continue #Restart the loop.
        break #Exit the loop when the valid year is entered.

    #Determine the maximum number of days allowed for the entered month and year.
    if month in [1, 3, 5, 7, 8, 10, 12]: #Months with 31 days.
        max_days = 31
    elif month in [4, 6, 9, 11]: #Months with 30 days.
        max_days = 30
    elif month == 2: #Special case: February.
        max_days = 29 if is_leap_year(year) else 28 #Leap year check using is_leap_year function.

    if not 1 <= date <= max_days: #Validate if the entered day is within the range for the determined max_days
        print(f"Invalid day for the given month and year. Re-enter the date.")
        return validate_date_input()  #Restart the process if the day is invalid

    return date, month, year


def validate_continue_input(): #Function to validate whether the user wants to continue or exit.
    
    while True: #Loop to ensure valid input
        again_date = input("Do you want to select another data file for a different date? Y/N: ").lower() #Prompt the user for input, remove whitespace, and convert to lowercase.
        if again_date == "y": #Check if the user input is 'y'.
            print("Loading a new data set...")
            return True   #Return True to indicate continuation.
        elif again_date == "n": # Check if the user input is 'n'.
            return False #Return False to indicate the program should stop.
        else:
            print("Invalid input. Please enter 'Y' for yes or 'N' for no.") #Provide feedback to the user about valid input options.


def process_csv_data(file_name): #Function to process a CSV file containing traffic data and extract required information.
    results = []

    try:
        with open(file_name, mode="r") as file:
            reader = csv.DictReader(file)

            # Variables to store statistics
            total_vehicles = 0
            total_trucks = 0
            electric_vehicles = 0
            two_wheeled_vehicles = 0
            busses_north = 0
            straight_vehicles = 0
            total_bicycles = 0
            over_speed_limit = 0
            elm_avenue_vehicles = 0
            hanley_highway_vehicles = 0
            scooters = 0
            # Hourly traffic statistics
            hourly_traffic = {}
            hanley_hourly_traffic = {}
            rain_hours = 0

            # Process each row
            for row in reader:
                try:
                    total_vehicles += 1

                    if row["VehicleType"] == "Truck": #Count trucks.
                        total_trucks += 1

                    if row["elctricHybrid"] == "True": #Count electric/hybrid vehicles.
                        electric_vehicles += 1

                    if row["VehicleType"] in ["Bicycle", "Motorcycle", "Scooter"]: #Count two wheeled vehicles.
                        two_wheeled_vehicles += 1

                    if (
                        "buss" in row["VehicleType"].strip().lower()
                        and row["travel_Direction_out"].strip().upper().startswith("N") #Count buses traveling north on Hanley Highway.
                        and "hanley highway" in row["JunctionName"].strip().lower()
                    ):
                        busses_north += 1

                    if row["travel_Direction_in"].strip().lower() == row["travel_Direction_out"].strip().lower(): #Count vehicles going stright.(same direction in and out).
                        straight_vehicles += 1

                    if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]): #Count vehicles going over the speed limit.
                        over_speed_limit += 1

                    if row["JunctionName"].strip().lower() == "elm avenue/rabbit road": #Count vehicles at elm avenue/rabbit road.
                        elm_avenue_vehicles += 1
                        if row["VehicleType"].strip().lower() == "scooter": #Nested condition to count scooters specifically at the same junction.
                            scooters += 1

                    if row["JunctionName"].strip().lower() == "hanley highway/westway": #Count vehicles at Hanley Highway/Westway junction
                        hanley_highway_vehicles += 1
                        hour = row["timeOfDay"][:2] #Retrieves the time (ex. "13:45:30") as a string & uses slicing to extract the first two characters of the string (ex. 13:45:30 -> 13).
                        hanley_hourly_traffic[hour] = hanley_hourly_traffic.get(hour, 0) + 1 #Update the count of vehicles for the extracted hour in the hanley_hourly_traffic dictionary

                    if row["VehicleType"].strip().lower() == "bicycle":  #Count bicycles.
                        total_bicycles += 1

                    hour = row["timeOfDay"][:2] #Update hourly traffic for all vehicles
                    hourly_traffic[hour] = hourly_traffic.get(hour, 0) + 1

                    if row["Weather_Conditions"].strip().lower() in ["heavyrain", "light rain"]: #Counting the rain hours.
                        rain_hours += 1

                except KeyError as e:
                    print(f"Missing expected key in row: {e}")
                except ValueError as e:
                    print(f"Error processing row values: {e}")

            # Post-processing calculations
            truck_percentage = round((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0 #Calculating the Truck percentage of total vehicles.
            avg_bikes_per_hour = total_bicycles / 24 if total_bicycles > 0 else 0 #Calculate average number of bikes.
            peak_hour = max(hourly_traffic, key=hourly_traffic.get, default="00") #Determine the peak hour for total traffic.
            peak_hour_count = hourly_traffic.get(peak_hour, 0)

            hanley_peak_hour = max(hanley_hourly_traffic, key=hanley_hourly_traffic.get, default=None) #Find the hour with the highest traffic in the hanley_hourly_traffic dictionary.
            hanley_peak_count = hanley_hourly_traffic.get(hanley_peak_hour, 0) if hanley_peak_hour else 0 #Handle the case if hanley_hourly_traffic is empty.

            # Generate results
            results.append(f"The name of the selected CSV file {file_name}")
            results.append(f"The total number of vehicles passing through all junctions for the selected date {total_vehicles}")
            results.append(f"The total number of trucks passing through all junctions for the selected date {total_trucks}")
            results.append(f"The total number of electric vehicles passing through all junctions for the selected date {electric_vehicles}")
            results.append(f"The number of “two wheeled” vehicles through all junctions for the date (bikes, motorbike, scooters) {two_wheeled_vehicles}")
            results.append(f"The total number of busses leaving Elm Avenue/Rabbit Road junction heading north {busses_north}")
            results.append(f"The total number of vehicles passing through both junctions without turning left or right {straight_vehicles}")
            results.append(f"The percentage of all vehicles recorded that are Trucks for the selected  {truck_percentage}%")
            results.append(f"Average number of bicycles per hour {int(avg_bikes_per_hour)}")
            results.append(f"The total number of vehicles recorded as over the speed limit for the selected date {over_speed_limit}")
            results.append(f"The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date {elm_avenue_vehicles}")
            results.append(f"The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date {hanley_highway_vehicles}")
            results.append(f"The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters {int((scooters / elm_avenue_vehicles) * 100) if elm_avenue_vehicles > 0 else 0}%")
            results.append(f"The total number of hours of rain on the selected date {rain_hours}")
            results.append(f"Peak hour: Between {peak_hour}:00 and {int(peak_hour) + 1}:00 with {peak_hour_count} vehicles")
            if hanley_peak_hour:
                results.append(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {hanley_peak_count} during {hanley_peak_hour}:00-{int(hanley_peak_hour) + 1}:00")
            else:
                results.append("The highest number of vehicles in an hour on Hanley Highway/Westway is 0")

    except FileNotFoundError: #Handle any file or data-related exceptions.
        results.append(f"File not found: {file_name}.")
    except Exception as e:
        results.append(f"An error occurred: {e}")
    return results


def display_outcomes(outcomes): #Function to display the processed results line by line.
    for line in outcomes:
        print(line) #Iterate through each line in the outcomes list and print it.


def save_results_to_file(outcomes, file_name="results.txt"): #Function to save the processed results to a file.
    try:
        with open(file_name, mode="a") as file: #Open the specified file in append mode. Default file name is "results.txt".
            for line in outcomes:
                file.write(line + "\n") #Write each line from the outcomes list to the file.
            file.write("\n" + "*" * 80 + "\n\n") #Add a separator after each set of results.
        print(f"Results successfully saved to {file_name}.") #Notify the user that results were saved successfully.
    except Exception as e: #Handle any errors.
        print(f"An error occurred while saving results to file: {e}")


def main(): #Main function that runs the Traffic Data Analysis Program.
    print("Welcome to the 'TRAFFIC ANALYSIS PROGRAM 2024'")
    while True: #Start an infinite loop to allow continuous analysis until the user decides to stop.
        day, month, year = validate_date_input()
        file_name = f"traffic_data{int(day):02d}{int(month):02d}{int(year)}.csv" #Construct the filename for the CSV file based on the provided date.
        results = process_csv_data(file_name) #Process the data from the CSV file and store the results in a list.
        display_outcomes(results) #Display the results to the user.
        save_results_to_file(results) #Save the results to a file.
        if not validate_continue_input():
            break #Exit the loop if the user does not want to continue.
    print("Exiting the program. Thank you!") #Final message to thank the user for using the program.


if __name__ == "__main__": #Executes the main() function when the script is run.
    main()
# if you have been contracted to do this assignment please do not remove this line.
