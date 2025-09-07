from bisect import insort_left
from collections import deque
from dataclasses import dataclass
from enum import IntEnum


class ImageType(IntEnum):
    EMBEDDED = 0
    SURROUNDED = 1
    FLOATING = 2


@dataclass
class Image:
    width: int
    height: int
    dx: int
    dy: int
    type : ImageType

class Fragment:
    def __init__(self, width, dx):
        self.remain_w = width
        self.w = width
        self.dx = dx
        self.is_first = True
        self.right_corner_x = dx
        self.right_corner_y = 0

    def checkCapacity(self, token_width, is_sur):
        if self.is_first or is_sur:
            return token_width <=  self.remain_w
        return token_width + char_w <= self.remain_w

    def addWord(self, width):
        if self.is_first:
            self.remain_w -= width
            self.is_first = False
        else:
            self.remain_w -= width + char_w
        self.right_corner_x = self.dx + self.w - self.remain_w
        self.right_corner_y = 0
    def addEmbeddedImage(self, image):
        if self.is_first:
            image.dx = self.dx+ self.w - self.remain_w
            self.remain_w -= image.width
            self.is_first = False
        else:
            image.dx = self.dx + self.w - self.remain_w + char_w
            self.remain_w -= image.width + char_w
        self.right_corner_x = self.dx +self.w - self.remain_w
        self.right_corner_y = 0

    def addSurroundedImage(self, image):
        image.dx = self.dx + self.w - self.remain_w
        self.remain_w -= image.width
        self.is_first = True
        self.right_corner_x = self.dx + self.w - self.remain_w
        self.right_corner_y = 0

    def addFloatingImage(self, image, absolute_y):
        if self.right_corner_x + image.dx >= 0:
            if self.right_corner_x + image.dx + image.width <=file_width:
                image.dx = self.right_corner_x + image.dx
            else:
                shift = self.right_corner_x + image.dx + image.width - file_width
                image.dx = self.right_corner_x + image.dx -shift
        else:
            image.dx = 0

        self.right_corner_x = image.dx + image.width
        self.right_corner_y = image.dy + self.right_corner_y
        image.dy = absolute_y + self.right_corner_y


class FileString:
    def __init__(self, images):
        self.h = file_height
        self.fragments = deque()
        self.createFragments(images)

    def createFragments(self, images):
        if images:
            if images[0].dx != 0:
                self.fragments.append(Fragment(images[0].dx, 0))
            for i in range(len(images) - 1):
                new_w = images[i+1].dx - images[i].dx - images[i].width
                if new_w != 0:
                    self.fragments.append(Fragment(new_w, images[i].dx + images[i].width ))

            right_corner = images[-1].dx + images[-1].width
            if right_corner != file_width:
                self.fragments.append(Fragment(file_width - right_corner, right_corner))
        else:
            self.fragments.append(Fragment(file_width, 0))


    def addWord(self, width):
        while self.fragments:
            cur_fr = self.fragments[0]
            if cur_fr.checkCapacity(width, False):
                cur_fr.addWord(width)
                return True
            self.fragments.popleft()
        return False

    def addEmbeddedImage(self, image):
        while self.fragments:
            cur_fr = self.fragments[0]
            if cur_fr.checkCapacity(image.width, False):
                cur_fr.addEmbeddedImage(image)
                self.h = max(self.h, image.height)
                return True
            self.fragments.popleft()
        return False

    def addSurroundedImage(self, image):
        while self.fragments:
            cur_fr = self.fragments[0]
            if cur_fr.checkCapacity(image.width, True):
                cur_fr.addSurroundedImage(image)
                return True
            self.fragments.popleft()
        return False

    def addFloatingImage(self, image, absolute_y):
        self.fragments[0].addFloatingImage(image, absolute_y)


class Paragraph:
    def __init__(self, dy):
        self.h = 0
        self.dy = dy
        self.images = []
        self.strings = [FileString(self.images)]


    def addString(self):
        self.h += self.strings[-1].h
        self.refreshImages()
        self.strings.append(FileString(self.images))

    def refreshImages(self):
        new_images = []
        for image in self.images:
            if self.dy + self.h < image.dy + image.height:
                new_images.append(image)
        self.images = new_images

    def addWord(self, width):
        while not self.strings[-1].addWord(width):
            self.addString()

    def addImage(self, image):
        match image.type:
            case ImageType.EMBEDDED:
                while not self.strings[-1].addEmbeddedImage(image):
                    self.addString()
                image.dy = self.dy + self.h

            case ImageType.SURROUNDED:
                while not self.strings[-1].addSurroundedImage(image):
                    self.addString()
                image.dy = self.dy + self.h
                insort_left(self.images, image, key=lambda elem:elem.dx)

            case ImageType.FLOATING:
                self.strings[-1].addFloatingImage(image, self.dy+self.h)

        print(image.dx, image.dy)

    def endParagraph(self):
        self.addString()
        if self.images:
            max_h = max(self.images, key=lambda elem:elem.dy+ elem.height)
            diff = max_h.dy + max_h.height - self.h
            if diff >0:
                self.h += diff


class File:
    def __init__(self):
        self.h = 0
        self.parags = [Paragraph(0)]

    def parserString(self, string):
        token_w = 0
        is_emp = True
        i = 0
        while i < len(string):
            if string[i] not in " \t\n":
                is_emp = False
                if string[i] != "(":
                    token_w += char_w
                    i +=1
                else:
                    new_i = string.find(")", i+1)
                    image = self.parseString2Image(string, i+1, new_i)
                    self.parags[-1].addImage(image)
                    i = new_i +1
            else:
                if token_w !=0:
                    self.parags[-1].addWord(token_w)
                    token_w = 0
                i += 1
        if token_w != 0:
            self.parags[-1].addWord(token_w)

        if is_emp:
            self.parags[-1].endParagraph()
            self.h += self.parags[-1].h
            self.parags.append(Paragraph(self.h))


    def parseString2Image(self, string, start, end):
        image_str = string[start:end].split()[1:]

        key_val = [elem.split('=') for elem in image_str]
        dx = dy = 0
        for key, val in key_val:
            match key:
                case "layout":
                    if val == "embedded":
                        image_type = ImageType.EMBEDDED
                    elif val == "surrounded":
                        image_type = ImageType.SURROUNDED
                    else:
                        image_type = ImageType.FLOATING
                case "width":
                    width = int(val)

                case "height":
                    height = int(val)

                case "dx":
                    dx = int(val)

                case "dy":
                    dy = int(val)

        return Image(width, height, dx,dy, image_type)


with open('input.txt', 'r') as fl:
    file_width, file_height, char_w = map(int, fl.readline().split())
    file = File()
    lines = []
    cur_line = ""
    for line in fl:
        if not line.rstrip():
            lines.append(cur_line)
            lines.append("")
            cur_line = ""
        else:
            cur_line += " " + line.rstrip()
    lines.append(cur_line)

    for line in lines:
        file.parserString(line)
    d = 0







