from image_manipulation.imagemanipulation import ImageManipulation
from PIL import Image


class PillowImageManipulation(ImageManipulation):
    def execute_manipulation(self, image: Image) -> Image:
        raise NotImplementedError
