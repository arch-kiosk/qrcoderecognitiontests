from PIL.Image import Image
from functools import reduce
import PIL

from pillowimagemanipulation import PillowImageManipulation
import numpy


class PillowBitplaneManipulation(PillowImageManipulation):
    def get_parameters(self):
        return []

    def __init__(self, bitmask: int = 255):
        self.bitmask = bitmask

    def execute_manipulation(self, image: Image) -> Image:

        np_array = numpy.array(image)
        return PIL.Image.fromarray(numpy.bitwise_and(np_array, self.bitmask))


