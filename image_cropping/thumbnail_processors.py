def crop_corners(image, box=None, **kwargs):
    """
    Crop at defined corners, saved as promille values
    """
    if box:
        values = [int(x) for x in box.split(',')]
        rx, ry = image.size
        rx = rx / 1000.0
        ry = ry / 1000.0
        box = (
            int(values[0] * rx),
            int(values[1] * ry),
            int(values[2] * rx),
            int(values[3] * ry),
        )
        image = image.crop(box)

    return image
