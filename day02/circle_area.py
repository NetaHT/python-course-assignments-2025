import math

def calculate_circle_area(radius):
    # Calculate the area using π r²
    area = math.pi * (radius ** 2)
    return round(area, 2)

# Run the function if the script is run directly
if __name__ == "__main__":
    radius = float(input("Enter the radius of the circle: "))
    area = calculate_circle_area(radius)
    print(f"The area of the circle is: {area}")
