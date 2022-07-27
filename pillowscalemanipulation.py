from PIL.Image import Image
from PIL import ImageEnhance
from PIL.Image import LANCZOS
from pillowimagemanipulation import PillowImageManipulation


class PillowScaleManipulation(PillowImageManipulation):
    def __init__(self, scalefactor: float):
        self.scalefactor = scalefactor

    def execute_manipulation(self, image: Image) -> Image:

        new_width = int(image.width * self.scalefactor)
        new_height = int(image.height * self.scalefactor)

        return image.resize((new_width, new_height), LANCZOS)
