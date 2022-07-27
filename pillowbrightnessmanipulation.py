from PIL.Image import Image
from PIL import ImageEnhance
from pillowimagemanipulation import PillowImageManipulation


class PillowBrightnessManipulation(PillowImageManipulation):
    def __init__(self, enhance: int):
        self.enhance = enhance

    def execute_manipulation(self, image: Image) -> Image:

        return ImageEnhance.Brightness(image).enhance(self.enhance)

    def get_parameters(self):
        return ["brighter", self.enhance]
