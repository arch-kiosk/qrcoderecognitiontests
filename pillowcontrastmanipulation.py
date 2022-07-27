from PIL.Image import Image
from PIL import ImageEnhance
from pillowimagemanipulation import PillowImageManipulation


class PillowContrastManipulation(PillowImageManipulation):
    def __init__(self, enhance: int):
        self.contrast_enhance = enhance

    def execute_manipulation(self, image: Image) -> Image:

        return ImageEnhance.Contrast(image).enhance(self.contrast_enhance)

    def get_parameters(self):
        return ["factor", self.contrast_enhance]
