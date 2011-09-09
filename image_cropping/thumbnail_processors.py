def crop_corners(image, box=None, **kwargs):
    """
    Crop corners to the selection defined by image_cropping
    """

    if box:
        values = [int(x) for x in box.split(',')]
        box = (
            int(values[0]),
            int(values[1]),
            int(values[2]),
            int(values[3]),
        )
        image = image.crop(box)

    return image

