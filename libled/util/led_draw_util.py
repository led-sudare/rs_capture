import numpy as np
from PIL import Image, ImageDraw


def get_scled_rgb_image(src, wscale, hscale):
    image = Image.fromarray(src, 'RGB')
    nw = int(round(image.width * wscale))
    nh = int(round(image.height * hscale))
    scaled = image.resize((nw, nh))
    scaled = scaled.rotate(Image.ROTATE_90)
    return np.asarray(scaled)


def resize2(src, new_size, pos, fill):
    dx, dy, sx, sy, w, h = get_copy_positions(new_size, src.shape, pos)

    new_src = src
    pad = None
    if dx > sx:
        pad = np.array([[fill * h] * dx])
        new_src = np.vstack([pad[0, :, :, :], new_src])

    if new_size[0] > dx + w:
        pad = np.array([[fill * h] * (new_size[0] - dx - w)])
        new_src = np.vstack([new_src, pad[0, :, :, :]])

    if dy > sy:
        pad = np.array([[fill * dy] * new_size[0]])
        new_src = np.hstack([pad[0, :, :, :], new_src])

    if new_size[1] > dy + h:
        pad = np.array([[fill * (new_size[1] - dy - h)] * new_size[0]])
        new_src = np.hstack([new_src, pad[0, :, :, :]])

    if src.shape[0] > new_size[0]:
        new_src = new_src[sx:sx+w, :]

    if src.shape[1] > new_size[1]:
        new_src = new_src[:, sy:sy+h]

    return new_src


def get_copy_positions(src_size, dst_size, pos):
    dw = dst_size[0]
    dh = dst_size[1]
    sw = src_size[0]
    sh = src_size[1]

    w = min(dw, sw)
    h = min(dh, sh)

    dx = pos[0]
    dy = pos[1]
    sx = sy = 0

    if pos[0] < 0:
        dx = 0
        sx = -pos[0]

    if pos[1] < 0:
        dy = 0
        sy = -pos[1]

    return (dx, dy, sx, sy, w, h)
