def dateValidation():
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 > day or day > 31:
                print("Invalid date")
                continue
            else:
                break
        except ValueError:
            print("Integer required")
            continue

    while True:
        try:
            month = int(input("Please enter the day of the survey in the format dd: "))
            if 1 > month or month > 12:
                print("Out of range - values must be in the range 1 to 12.")
                continue
            else:
                break
        except ValueError:
            print("Integer required")
            continue

    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 > year or year > 2025:
                print("Out of range - values must range from 2000 and 2024.")
                continue
            else:
                break
        except ValueError:
            print("Integer required")
            continue

        return day, month, year

def main():
    day, month, year = dateValidation()
    print(f"Day: {day}, Month: {month}, Year: {year}")

if __name__ == "__main__":
    main()