from PIL import Image, ImageFilter, ImageDraw, ImageFont
import math

def avg_rgb(image):
    r, g, b = 0, 0, 0
    count = 0
    imgData = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            tempr, tempg, tempb = imgData[x, y]
            r += tempr
            g += tempg
            b += tempb
            count += 1
    # calculate averages
    return (r / count), (g / count), (b / count)

def convert_255(c):
    return 127 + math.pow((c / 255.0), 1.0 / 2.5) * 128

def cut_by_h(img, h):
    width = float(img.size[0])
    height = float(img.size[1])

    scale = width / height
    w = scale * h
    return img.resize((int(w), int(h)), Image.ANTIALIAS)


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)

class AImage(object):
    base_img = 0
    rating_img = 0
    transparent_img = 0
    chara_img = 0
    clear_img = 0
    score_img = 0
    song_name = ''

    color = ''
    difficulty = ['PST', 'PRE', 'FTR']

    diff_rank = 2

    def __init__(self, names):
        self.song_name = names[0]
        self.base_img = Image.open(names[0])
        self.rating_img = Image.open(names[1])
        self.transparent_img = Image.open(names[2])
        self.chara_img = Image.open(names[3])
        self.clear_img = Image.open(names[4])
        self.score_img = Image.open(names[5])

        self.rating_img.resize((100, 100), Image.ANTIALIAS)
        self.base_img = self.base_img.point(lambda p: p * 0.616)
        self.base_img = self.base_img.filter(MyGaussianBlur(radius=30))
        r, g, b = avg_rgb(self.base_img)
        self.color = '#%02x%02x%02x' % (int(convert_255(r)), int(convert_255(g)), int(convert_255(b)))
    
    
    def text_border(self, draw, x, y, text, font, shadowcolor, fillcolor):
        # thin border
        b = 1
        draw.text((x - b, y), text, font=font, fill=shadowcolor)
        draw.text((x + b, y), text, font=font, fill=shadowcolor)
        draw.text((x, y - b), text, font=font, fill=shadowcolor)
        draw.text((x, y + b), text, font=font, fill=shadowcolor)
    
        # thicker border
        draw.text((x - b, y - b), text, font=font, fill=shadowcolor)
        draw.text((x + b, y - b), text, font=font, fill=shadowcolor)
        draw.text((x - b, y + b), text, font=font, fill=shadowcolor)
        draw.text((x + b, y + b), text, font=font, fill=shadowcolor)
    
        # now draw the text over it
        draw.text((x, y), text, font=font, fill=fillcolor)

        return draw


    def create_img(self, info):
        print(info)

        draw = ImageDraw.Draw(self.base_img)
        base = 283
        inc = 44
        font = ImageFont.truetype('Hack/Hack Regular Nerd Font Complete Mono Windows Compatible.ttf', 24)
        if (len(info['song_name']) > 16):
            info['song_name'] = info['song_name'][:14] + '..'
        draw.text((144, 138), info['song_name'] + '  (' + self.difficulty[int(info['difficulty'])] + ')', fill=self.color, font=font)
        
        draw.text((250, base), 'Pure  ' + info['pure'], fill=self.color, font=font)
        draw.text((250, base + inc * 1), 'Far   ' + info['far'], fill=self.color, font=font)
        draw.text((250, base + inc * 2), 'Miss  ' + info['miss'], fill=self.color, font=font)
        draw.text((250, base + inc * 3), 'Ptt   ' + str(info['ptt']), fill=self.color, font=font)
        draw.text((250, base + inc * 4), 'Date  ' + info['date'], fill=self.color, font=font)

        self.base_img.paste(self.rating_img, (382, 25), self.rating_img)
        font = ImageFont.truetype('GeosansLight.ttf', 45)
        draw.text((130, 30), info['name'], fill=self.color, font=font)
        font = ImageFont.truetype('GeosansLight.ttf', 40)
        draw.text((144, 210), info['score'], fill=self.color, font=font)

        ptt_size = 48
        fill_color = '#FFEDF9'
        shadow_color = '#776875'

        draw = ImageDraw.Draw(self.transparent_img)
        font = ImageFont.truetype('Exo-Regular.ttf', ptt_size)
        plist = info['rank'].split('.')
        pttw = font.getsize(plist[0])[0]
        draw = self.text_border(draw, 430 - pttw, 48, plist[0] + '.', font, shadow_color, fill_color)
        font = ImageFont.truetype('Exo-Regular.ttf', int(ptt_size * 0.75))
        draw = self.text_border(draw, 445, 60, plist[1], font, shadow_color, fill_color)
        self.base_img.paste(self.transparent_img, (0, 0), self.transparent_img)

        self.chara_img = self.chara_img.resize((87, 87), Image.ANTIALIAS)
        self.base_img.paste(self.chara_img, (25, 15), self.chara_img)

        self.clear_img = cut_by_h(self.clear_img, 64)
        clear_base = 72 - int(self.clear_img.size[0] / 2)
        self.base_img.paste(self.clear_img, (clear_base, 120), self.clear_img)

        self.score_img = cut_by_h(self.score_img, 52)
        score_base = 72 - int(self.score_img.size[0] / 2)
        self.base_img.paste(self.score_img, (score_base, 207), self.score_img)

        song_img = Image.open(self.song_name)
        song_img = song_img.resize((196, 196), Image.ANTIALIAS)
        self.base_img.paste(song_img, (28, 287))

        self.base_img.resize((425, 425), Image.ANTIALIAS)
        return self.base_img