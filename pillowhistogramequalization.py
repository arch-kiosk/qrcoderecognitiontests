from PIL.Image import Image
from PIL.ImageOps import equalize
from functools import reduce
import PIL

from pillowimagemanipulation import PillowImageManipulation
import numpy as np


class PillowHistogramEqualization(PillowImageManipulation):
    def get_parameters(self):
        return []

    import numpy as np

    @staticmethod
    def numpy_image_histogram_equalization(image, number_bins=256):
        # from http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html

        # get image histogram
        image_histogram, bins = np.histogram(image.flatten(), number_bins, density=True)
        cdf = image_histogram.cumsum()  # cumulative distribution function
        cdf = 255 * cdf / cdf[-1]  # normalize

        # use linear interpolation of cdf to find new pixel values
        image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

        return image_equalized.reshape(image.shape)

    def execute_manipulation(self, image: Image) -> Image:

        # np_array = np.array(image)
        #
        # new_img = PIL.Image.fromarray(self.numpy_image_histogram_equalization(np_array))
        # return new_img.convert("L")
        return equalize(image)

