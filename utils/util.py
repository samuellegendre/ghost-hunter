import pyglet.image


def center_image(image):
    if isinstance(image, pyglet.image.Animation):
        x = image.get_max_width() / 2
        y = image.get_max_height() / 2
        for frame in image.frames:
            img = frame.image
            img.anchor_x = x
            img.anchor_y = y
    else:
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2


def check_bounds(image):
    min_x = -image.width
    max_x = image.width - 3

    if image.x < min_x:
        image.x = max_x
    if image.x > max_x:
        image.x = min_x


def get_rectangle(self):
    left = self.x - self.width / 2
    right = self.x + self.width / 2
    top = self.y + self.height / 2
    bottom = self.y - self.height / 2
    lt = (left, top)
    rt = (right, top)
    lb = (left, bottom)
    rb = (right, bottom)

    return lt, rt, rb, lb
