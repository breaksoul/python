import tesserocr#图片识别的库
from PIL import Image
image=Image.open("tupian.jpg")
result=tesserocr.image_to_text(image)
print (result)
#有些图片需要进行额外处理，提高识别成功率去掉多余干扰线条
image=image.convert('L')#将图像转化为灰度图像

image=image.convert('1')#将图像进行二值化处理，同事还可以指定二值化的阈值（也就是把图像灰度之后，将图像变为0-255的黑海图，只要高于某个值，可以认定为有效的，低于的就可以抛弃））
threshold=80#指定阈值
#完整代码附上

image = image.convert('L')
threshold = 80
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
 
image = image.point(table, '1')#将阈值为1的组成图片，达到清洗目的
image.show()
result = tesserocr.image_to_text(image)
print(result)