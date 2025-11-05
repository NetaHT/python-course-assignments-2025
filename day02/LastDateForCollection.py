#this file calculates the date 18 days before a given date provided via user input
#user input format: DD/MM/YYYY

from datetime import datetime, timedelta

def calculate_last_date_for_collection():
    # Ask user for input date in DD/MM/YYYY format
    date_str = input("Please enter a date (DD/MM/YYYY): ")
    
    try:
        # Convert string to datetime object
        input_date = datetime.strptime(date_str, "%d/%m/%Y")
        
        # Calculate date 18 days before
        result_date = input_date - timedelta(days=18)
        
        # Format and return the result
        return result_date.strftime("%d/%m/%Y")
    except ValueError:
        return "Error: Please enter a valid date in the format DD/MM/YYYY"

if __name__ == "__main__":
    result = calculate_last_date_for_collection()
    print(f"The date 18 days before your input date is: {result}")