import Expressions
from PIL import Image
import sys


class RandomArtImage:
    def __init__(self, depth):
        self.root_expr = Expressions.EExpression(depth)

    def _sample_expression(self, x, y):
        # Base output, on [-1,1]
        normalized_rgb_out = self.root_expr.evaluate(x, y)
        # Translation from [-1, 1] -> [0, 255]
        rgb_ints = [round((norm_val+1)*(255/2.0)) for norm_val in normalized_rgb_out]
        return rgb_ints

    def render(self, size, filename_out):
        im = Image.new('RGB', (size, size))

        # Derive the distance in image space needed to span [-1,1] with the correct number of pixels
        min_val = -1
        max_val = 1
        delta = (max_val - min_val) / (size - 1)

        # x_out and y_out: pixel locations in rendered image
        # x and y: locations in the random art [-1,1] continuum
        for x_out in range(size):
            x = min_val + delta * x_out
            for y_out in range(size):
                y = min_val + delta * y_out
                r, g, b = self._sample_expression(x, y)
                im.putpixel((x_out, y_out), (r, g, b))

        im.save(filename_out)
        im.close()


def main(argv):
    size = int(argv[1])
    depth = int(argv[2])
    filename_out = argv[3]
    random_art = RandomArtImage(depth)
    random_art.render(size, filename_out)


if __name__ == '__main__':
    main(sys.argv)
