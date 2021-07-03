import sys


class LIGHT:
    black = "\x1b[90m"
    red = "\x1b[91m"
    green = "\x1b[92m"
    white = "\x1b[97m"


END = "\x1b[0m"
pixel_row = ""
pixel_rows = []


def reproduce_image(path_to_img):  # create img array
    from PIL import Image
    try:
        image = Image.open(path_to_img)
    except FileNotFoundError:
        exit(LIGHT.red + "\n!!! Image doesn\'t exist, check for error !!!" + END)
    image = image.resize((50, 20), Image.ANTIALIAS)
    image.save("new.png")


def create_image(path_to_img, width, height):  # create img array
    from PIL import Image
    from numpy import asarray
    try:
        image = Image.open(path_to_img)
    except FileNotFoundError:
        exit(LIGHT.red + "\n!!! Image doesn\'t exist, check for error !!!" + END)
    image = image.resize((width, height), Image.ANTIALIAS)  # (w,h)
    return asarray(image)


def rgb_xterm(r, g, b):  # converts RGB to xterm 256
    if r == g == b:
        if r < 8:
            return str(16)
        if r > 248:
            return str(231)
        return str(round(((r - 8) / 247) * 24) + 232)
    return str(16 + (36 * round(r / 255 * 5)) +
               (6 * round(g / 255 * 5)) +
               round(b / 255 * 5))


def rgb_xterm_array(r, g, b):  # converts RGB to xterm RGB values
    if r == g == b:
        if r < 8:
            return str(16)
        if r > 248:
            return str(231)
        return str(round(((r - 8) / 247) * 24) + 232)
    return [
        16 + (36 * round(r / 255 * 5)),
        (6 * round(g / 255 * 5)),
        round(b / 255 * 5)
    ]


def print_image(image):  # prints image pixels
    rows, columns, _ = image.shape
    global pixel_row
    for x in range(rows):
        print('   ', end='')
        for y in range(columns):
            r, g, b = image[x][y]
            pixel_row += "\x1b[48;5;{}m \x1b[0m".format(str(rgb_xterm(r, g, b)))
        print(pixel_row, end='', flush=True)
        pixel_row = ""
        print('')


def write_image(image):  # write img to output file
    import os
    rows, columns, _ = image.shape
    global pixel_row
    global pixel_rows
    abs_path = os.path.join(os.path.dirname(__file__), ".assist/.plew")
    with open(abs_path, "w") as file:
        for x in range(rows):
            for y in range(columns):
                r, g, b = image[x][y]
                pixel_row += "\x1b[48;5;{}m \x1b[0m".format(rgb_xterm(r, g, b))
            pixel_rows.append(pixel_row)
            pixel_row = ""
        file.write('\n'.join(pixel_rows))


def read_image(output_file):  # read output file
    with open(output_file, "r") as file:
        print(file.read())


def print_256():  # show all 256 colors
    for i in range(256):
        print("\x1b[48;5;%dm %d \x1b[0m|" % (i, i), end='')
    print()


if __name__ == '__main__' and len(sys.argv) == 3:
    file = sys.argv[2]
    if sys.argv[1] == "read":
        read_image(file)
    elif sys.argv[1] == "write":
        write_image(create_image(file, sys.argv[3], sys.argv[4]))
    elif sys.argv[1] == "print":
        print_image(create_image(file, sys.argv[3], sys.argv[4]))
    elif sys.argv[1] == "reproduce":
        reproduce_image(file)
    elif sys.argv[1] == "matrix":
        import numpy
        numpy.set_printoptions(threshold=sys.maxsize)
        print(create_image(file, sys.argv[3], sys.argv[4]))  # > matrix.txt
    elif sys.argv[1] == "rgb256":
        r, g, b = map(int, sys.argv[2].split(','))
        print(r, g, b)
        print(rgb_xterm_array(r, g, b))
        print(rgb_xterm(r, g, b))
elif len(sys.argv) == 2 and sys.argv[1] == "showall":
    print_256()


""" ANSI Escape Code: https://notes.burke.libbey.me/ansi-escape-codes/
    \x1b[48;5;{}m \x1b[0m
    \x1b[           - call function
    48;5;{}         - function parameters... 48;5;{} set bg to {}
    m               - function name... m: set graphic
    48;5;{}m        - function example: m(48, 5, {})
    \x1b[0m         - function m(0) to turn off control sequence
    The space between the beginning and ending control sequences
    includes space character to color just the background """
