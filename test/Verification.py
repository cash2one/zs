import pytesseract

from PIL import Image

import numpy

import pandas


#
# def initTable(threshold=200):
#     table = []
#     for i in range(256):
#         if i < threshold:
#             table.append(0)
#         else:
#             table.append(1)
#     return table
#
# image = Image.open('2.png')
# im = image.convert('L')
# binaryImage = im.point(initTable(), '1')
# binaryImage.show()
# print(pytesseract.image_to_string(binaryImage, config='-psm 10'))



#
#
# def rgb(im):
#     '''获取每一个像素的亮度     (r+g+b)/3
#     '''
#     width, heigth = im.size
#     data = numpy.zeros((heigth, width))
#     aa = []
#     for w in range(width):
#         for h in range(heigth):
#             y, cb, cr = im.getpixel((w, h))
#             data[h, w] = (y + cb + cr) / 3
#             aa.append((y + cb + cr) / 3)
#     data = pandas.DataFrame(data)
#     aa = pandas.Series(aa)
#     return aa, data
#
# def topliangdu(liangdu, biaozhun=100):
#     '''根据亮度排序，取大于标准的值
#     '''
#     c=liangdu.value_counts()
#     return list(c[c>100].index)
#
# def liangdutianbai(im,mubiao):
#     '''将非目标区域填充白色'''
#     width, heigth = im.size
#     for w in range(width):
#         for h in range(heigth):
#             y,cb,cr=im.getpixel((w,h)) #提取点(10,10)位置的亮度、蓝色分量、红色分量的值。
#             tmp = (y+cb+cr)/3
#             if tmp not in mubiao:
#                 im.putpixel([w,h],(255, 255, 255))
#     return im
#
#
#
# def tongse(im):
#     '''验证码验证文字的单个文字同色时，处理。'''
#     global aa, data
#     aa,data = rgb(im)
#     mubiao = topliangdu(aa)
#     im = liangdutianbai(im, mubiao)
#     img_grey = im.convert('L')
#     # img_grey.show()
#     return img_grey
#
# im = Image.open('2.png')
# text = pytesseract.image_to_string(tongse(im))  # 将图片转成字符串
# print(text)
#
#
#


from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import sys
# from pytesser3 import image_to_string
import pytesseract

# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

        # 由于都是数字
# 对于识别成字母的 采用该表进行修正
rep = {'O': '0',
       'I': '1', 'L': '1',
       'Z': '2',
       'S': '8'
       }


def getverify1(name):
    # 打开图片
    im = Image.open(name)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save('g' + name)
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    out.save('b' + name)
    # 识别
    text = pytesseract.image_to_string(out)
    # 识别对吗
    text = text.strip()
    text = text.upper()
    for r in rep:
        text = text.replace(r, rep[r])
        # out.save(text+'.jpg')
    print(text)
    return text


getverify1('2.png')