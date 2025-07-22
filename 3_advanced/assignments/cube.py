# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2025-07-15
# author  = Maxime Lecompte
#************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""

#Parent Class
class Object:
    def __init__(self, name):
        self.name = name
        self.translation_values = [0.0, 0.0, 0.0]
        self.rotation_values = [0.0, 0.0, 0.0]
        self.scale_values = [1.0, 1.0, 1.0]
        self.color_RGB = [255, 255, 255]  # Default color white

    def translate(self, x, y, z):
        self.translation_values = [x, y, z]
        #Print can be added when debugging
        #Ex: print(f"{self.name} translated to {self.translation_values}")

    def rotate(self, x, y, z):
        self.rotation_values = [x, y, z]

    def scale(self, x, y, z):
        self.scale_values = [x, y, z]

    def color(self, r, g, b):
        self.color_RGB = [r, g, b]


class Cube(Object):
    def __init__(self, name):
        super().__init__(name)
   
    def color(self, R, G, B):
        self.color_RGB = [R, G, B]

    def print_status(self):
        print(f"Cube Name: {self.name}")
        print(f"Translate: {self.translation_values}")
        print(f"Rotate:    {self.rotation_values}")
        print(f"Scale:     {self.scale_values}")
        print(f"Color:     {self.color_RGB}")

    def update_transform(self, ttype, value):   
        transform_methods = {
            "translate": self.translate,
            "rotate": self.rotate,
            "scale": self.scale
            }
        transform_methods[ttype](*value)

cube1 = Cube("CubeA")
cube2 = Cube("CubeB")
cube3 = Cube("CubeC")

# Apply transforms to cube1
cube1.update_transform("translate", [1.0, 2.0, 3.0])
cube1.update_transform("rotate", [45.0, 0.0, 90.0])
cube1.update_transform("scale", [8, 17.5, 25.5])

cube1.color(255, 100, 0)

# Print status
cube1.print_status()
cube2.print_status()
cube3.print_status()
