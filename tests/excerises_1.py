# Import the math module to use the value of pi
import math

# Define a function to calculate the area of a circle
def calculate_circle_area(radius):
    area_circle = math.pi * (radius ** 2)
    area_rounded = round(area_circle, 2)
    return area_rounded

# Read the radius as a float from input
radius_input= input(" ")
radius = float(radius_input)

# Call the function with the radius and print the result
result = calculate_circle_area(radius)
print(result)




