from PIL.Image import Image
from functools import reduce
import PIL

from pillowimagemanipulation import PillowImageManipulation
from numpy import array


class PillowThresholdManipulation(PillowImageManipulation):
    def __init__(self, threshold: int=-1):
        self.threshold = threshold

    @staticmethod
    def get_max(lst):
        max_value = lst[0]
        max_pos = 0
        for v in range(len(lst)):
            if lst[v] > max_value:
                max_value = lst[v]
                max_pos = v

        return max_pos

    def calculate_threshold(self, image: Image) -> int:
        if image.mode != "L":
            image = image.convert(mode="L")
        hist = image.histogram()
        pixel_sum = reduce((lambda p_sum, y: p_sum + y), hist)

        avg = 0
        result = -1
        for x in range(len(hist)):
            avg = avg + hist[x]
            result = x
            if avg > int(pixel_sum / 2):
                break

        if result > 126:
            return self.get_max(hist[:255-result]) + 10
        else:
            return result + self.get_max(hist[result:]) - 10

    def execute_manipulation(self, image: Image) -> Image:

        if self.threshold == -1:
            threshold = self.calculate_threshold(image)
            print(f"Trying threshold: {threshold}")
        else:
            threshold = self.threshold

        np_array = array(image)
        np_array[np_array <= threshold] = 0
        np_array[np_array > threshold] = 255
        return PIL.Image.fromarray(np_array)


