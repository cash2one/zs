# coding:utf-8
import sys, os
from PIL import Image, ImageDraw
import pytesseract
# import tesseract



img = Image.open("/Users/xiaxiaodong/Downloads/62.jpeg").convert("L")

def binarizing(img,threshold): #input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

img = binarizing(img, 140)


def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1, h-1):
        for x in range(1, w-1):
            count = 0
            if pixdata[x, y-1] > 245:
                count = count + 1
            if pixdata[x, y+1] > 245:
                count = count + 1
            if pixdata[x-1, y] > 245:
                count = count + 1
            if pixdata[x+1, y] > 245:
                count = count + 1

            if pixdata[x+1, y+1] > 245:
                count = count + 1
            if pixdata[x+1, y-1] > 245:
                count = count + 1
            if pixdata[x-1, y+1] > 245:
                count = count + 1
            if pixdata[x-1, y-1] > 245:
                count = count + 1

            if count > 5:
                pixdata[x, y] = 255
    return img

img_first = depoint(img)
img_last = depoint(img_first)
# img_last.show()

# text = pytesseract.image_to_string(img)
# # 识别对吗
# text = text.strip()

""" 识别转换 """
rep = {
    ' ': '',
    '}': 'j',
    'l': 't',
    ']': 'j',
    '[': 'j',
    '{': 'j',
    'G': '6',
}


text = pytesseract.image_to_string(img_last)
print(text)
for r in rep:
    text = text.replace(r, rep[r])
if not text.isalnum():
    text = pytesseract.image_to_string(img, config="-l eng")
for r in rep:
    text = text.replace(r, rep[r])

list = []
str_rule = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in text:
    if i in str_rule:
        list.append(i)
answer = "".join(list)
print(answer)




