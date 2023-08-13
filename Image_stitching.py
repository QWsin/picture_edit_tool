import os
import cv2
import logging
from BackgroundGenerator import BackgroundGenerator

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(filename)s - line %(lineno)s]'
                                                ' - %(message)s')


LEFT_RIGHT_PADDING = 570
UP_DOWN_PADDING = 380
MIDDLE_PADDING = 100
PIC_WIDTH = 6000
PIC_HEIGHT = 4000
FINAL_WIDTH = PIC_WIDTH*2 + LEFT_RIGHT_PADDING*2 + MIDDLE_PADDING
FINAL_HEIGHT = PIC_HEIGHT*2 + UP_DOWN_PADDING*2 + MIDDLE_PADDING

x_pos = [UP_DOWN_PADDING, UP_DOWN_PADDING+PIC_HEIGHT+MIDDLE_PADDING]
y_pos = [LEFT_RIGHT_PADDING, LEFT_RIGHT_PADDING+PIC_WIDTH+MIDDLE_PADDING]

top_x = [x_pos[0], x_pos[0], x_pos[1], x_pos[1]]
top_y = [y_pos[0], y_pos[1], y_pos[0], y_pos[1]]


def group_pic_by_4(files: list):
    pics = []
    for file in files:
        if os.path.splitext(file)[1] in ['jpeg', 'jpg', 'png']:
            pics.append(file)
    result = []
    for index in range(0, len(pics), 4):
        result.append(pics[index:index+4])
    return result


def get_new_pic_path(pic_path, file_suffix):
    name, ext = os.path.splitext(pic_path)
    return os.path.join(os.path.dirname(name), os.path.basename(name)+file_suffix+ext)


def clip_image(img):
    height, width, _ = img.shape
    logging.debug('width: {}, height: {}'.format(width, height))
    if width < height:
        logging.debug('rotating image')
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        height, width, _ = img.shape
    if width*2 == height*3:
        return img
    elif width*2 < height*3:
        target_height = round(width*2/3)
        up_padding = (height - target_height) // 2
        down_padding = (height - target_height) - up_padding
        result_image = img[up_padding:height-down_padding, :]
        return result_image
    else:
        # width/height > 3:2
        target_width = round(height*3/2)
        left_padding = (width-target_width) // 2
        right_padding = (width-target_width) - left_padding
        result_image = img[:, left_padding:width-right_padding]
        return result_image


if __name__ == '__main__':
    pic_folder_path = input('please input your photo folder:')
    # pic_folder_path = 'C:\\Users\\Sponge Bob\\Pictures\\test\\stitch'
    canvas_template = BackgroundGenerator.generate(FINAL_HEIGHT, FINAL_WIDTH, 0)

    pics = os.listdir(pic_folder_path)
    pics = group_pic_by_4(pics)
    for index, pic_group in enumerate(pics):
        final_image = canvas_template
        for i in range(len(pic_group)):
            pic_path = os.path.join(pic_folder_path, pic_group[i])
            image = cv2.imread(pic_path)
            # fix width/height 固定宽高比为3:2(或者2:3)
            clipped_image = clip_image(image)
            # upscale 缩放大小
            if not clipped_image.shape == (PIC_WIDTH, PIC_HEIGHT, 3):
                upscale_image = cv2.resize(clipped_image, (PIC_WIDTH, PIC_HEIGHT))
            else:
                upscale_image = clipped_image
            # stitch the 4 picture together 四张拼在白色背景上
            height, width, _ = upscale_image.shape
            logging.debug('upscale width: {}, height: {}'.format(width, height))
            logging.debug('top_x[i] = {}, top_x[i]+height = {}'.format(top_x[i], top_x[i] + height))
            logging.debug('top_y[i] = {}, top_y[i]+width = {}'.format(top_y[i], top_y[i] + width))
            final_image[top_x[i]:top_x[i]+height, top_y[i]:top_y[i]+width] = upscale_image
        final_image_path = os.path.join(pic_folder_path, 'stitch_{}.jpg'.format(index))
        logging.info('writing to file: {}'.format(final_image_path))
        # final_image_path = final_image_path.replace('.jpg', '.png')
        cv2.imwrite(final_image_path, final_image)
    logging.info('FINISHED! Please find the result in the folder.')
    input('[press enter to close this...]')
