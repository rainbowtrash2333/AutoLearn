import easyocr

if __name__ == '__main__':
    # 创建reader对象
    reader = easyocr.Reader(['ch_sim'])
    # 读取图像
    result = reader.readtext(r'D:\temp\111.jpg')
    # 结果
    print(result)
