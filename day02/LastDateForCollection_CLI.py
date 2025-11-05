#this file calculates the date 18 days before a given date provided via command line argument
#command line format: python LastDateForCollection_CLI.py DD/MM/YYYY


from datetime import datetime, timedelta
import sys

def calculate_last_date_for_collection(date_str):
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
    if len(sys.argv) != 2:
        print("Usage: python LastDateForCollection_CLI.py DD/MM/YYYY")
        print("Example: python LastDateForCollection_CLI.py 05/11/2025")
        sys.exit(1)
        
    date_str = sys.argv[1]
    result = calculate_last_date_for_collection(date_str)
    print(f"The date 18 days before {date_str} is: {result}")