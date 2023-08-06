import cv2
import numpy as np


class BackgroundGenerator:
    @staticmethod
    def generate(_height, _width, _col):
        _background = np.ones((_height, _width, 3), dtype=np.uint8) * _col
        return _background


if __name__ == '__main__':
    width = int(input('please input width: '))
    height = int(input('please input height: '))
    col = int(input('please input color: '))
    print(type(col))
    background = BackgroundGenerator.generate(height, width, col)
    file_name = 'background_{}x{}_{}.jpg'.format(width, height, col)
    cv2.imwrite(file_name, background)
    print('output file name: {}'.format(file_name))
