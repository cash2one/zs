import pytesseract

from PIL import Image

import numpy

import pandas

import pytesseract

from PIL import Image

im = Image.open('2.png')

im = im.convert("P")

#打印颜色直方图
print(im.histogram())

his = im.histogram()
values = {}

for i in range(256):
    values[i] = his[i]

for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
    print(j,k)

threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)


def white_black(name):
    im = Image.open(name)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save('g' + name)
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    out.save('b' + name)

white_black("2.png")





#得到单个像素的集合
inletter = False
foundletter=False
start = 0
end = 0

letters = []

im2 = Image.open('b2.png')

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter=False

print(letters)

