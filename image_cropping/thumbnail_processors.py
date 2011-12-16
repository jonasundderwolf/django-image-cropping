def crop_corners(image, box=None, **kwargs):
    """
    Crop corners to the selection defined by image_cropping
    """

    if box:
        values = [int(x) for x in box.split(',')]
        width = abs(values[2] - values[0])
        height = abs(values[3] - values[1])
        if width != image.size[0] or height != image.size[1]:
            image = image.crop(values)

    return image

