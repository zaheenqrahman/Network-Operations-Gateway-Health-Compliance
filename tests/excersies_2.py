import math

a = int(input())

octahedron_area = 2 * math.sqrt(3) * (a ** 2)
octahedron_volume = (1/3) * math.sqrt(2) * (a ** 3)

print(round(octahedron_area, 2), round(octahedron_volume, 2))


