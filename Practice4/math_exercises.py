

# 1
import math

degree = 15
radian = degree * (math.pi / 180)
print(degree)
print(round(radian, 6))

# 2
import math

height = 5
base1 = 5
base2 = 6
area_trapezoid = ((base1 + base2) / 2) * height
print(height)
print(base1)
print(base2)
print(area_trapezoid)

# 3
import math

n_sides = 4
side_length = 25
area_polygon = (n_sides * pow(side_length, 2)) / (4 * math.tan(math.pi / n_sides))
print(n_sides)
print(side_length)
print(round(area_polygon))

# 4
import math 

base_p = 5
height_p = 6
area_parallelogram = float(base_p * height_p)
print(base_p)
print(height_p)
print(area_parallelogram)