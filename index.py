while True:
    try:
        day = input("Please enter the day of the survey in the format dd: ")
        if not day.isdigit():  
            print("Integer required!")
            continue
        day = int(day)  
        if day < 1 or day > 31:
            print("Day must be in the range of 1-31")
        else:
            break
    except ValueError:
        print("Invalid input")

while True:
    try:
        month = input("Please enter the month of the survey in the format MM: ")
        if not month.isdigit():  
            print("Integer required!")
            continue
        month = int(month)  
        if month < 1 or month > 12:
            print("Month must be in the range of 1-12")
        else:
            break
    except ValueError:
        print("Invalid input")

while True:
    try:
        year = input("Please enter the year of the survey in the format YYYY: ")
        if not year.isdigit():  
            print("Integer required!")
            continue
        year = int(year)  
        if year < 2000 or year > 2025:
            print("Year must be in the range of 2000-2025")
        else:
            break
    except ValueError:
        print("Invalid input")