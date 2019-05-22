import tensorflow as tf
import numpy as np


def bilinear_upsampler(tensor, new_shape):
	return tf.image.resize(tensor, new_shape)



#Reference : https://github.com/tadax/m2det/blob/master/utils/generate_priors.py
def generate_priors(num_scales=3, anchor_scale=2.0, image_size=320, shapes=[40, 20, 10, 5, 3, 1]):
    anchor_configs = {}
    for shape in shapes:
        anchor_configs[shape] = []
        for scale_octave in range(num_scales):
            for aspect_ratio in [(1, 1), (1.41, 0.71), (0.71, 1.41)]:
                anchor_configs[shape].append(
                    (image_size / shape, scale_octave / float(num_scales), aspect_ratio))

    boxes_all = []
    for _, configs in anchor_configs.items():
        boxes_level = []
        for config in configs:
            stride, octave_scale, aspect = config
            base_anchor_size = anchor_scale * stride * (2 ** octave_scale)
            anchor_size_x_2 = base_anchor_size * aspect[0] / 2.0
            anchor_size_y_2 = base_anchor_size * aspect[1] / 2.0
            x = np.arange(stride / 2, image_size, stride)
            y = np.arange(stride / 2, image_size, stride)
            xv, yv = np.meshgrid(x, y)
            xv = xv.reshape(-1)
            yv = yv.reshape(-1)
            boxes = np.vstack((yv - anchor_size_y_2, xv - anchor_size_x_2,
                               yv + anchor_size_y_2, xv + anchor_size_x_2))
            boxes = np.swapaxes(boxes, 0, 1)
            boxes_level.append(np.expand_dims(boxes, axis=1))
        boxes_level = np.concatenate(boxes_level, axis=1)
        boxes_level /= image_size
        boxes_all.append(boxes_level.reshape([-1, 4]))

    anchor_boxes = np.vstack(boxes_all)

    return anchor_boxes
