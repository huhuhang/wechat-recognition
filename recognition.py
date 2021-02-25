import cv2
import base64
import requests


ACCESS_TOKEN = '24.9fe297a886c240b2f0fbf055c47f6330.2592000.1616837425.282335-23708795'


def object_detect(image: str) -> dict:
    """图像主体检测识别

    Args:
        image (str): 图像地址

    Returns:
        dict: 图像主体坐标
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect"
    # 二进制方式打开图片文件
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    request_url = request_url + "?access_token=" + ACCESS_TOKEN
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


def crop_image(image: str, response: dict):
    """裁剪图像主体
    """
    result = response['result']
    # 主体坐标转换
    x0 = result['left']
    x1 = result['left'] + result['width']
    y0 = result['top']
    y1 = result['top'] + result['height']
    # 读取图像
    img = cv2.imread(image)
    print(img.shape)
    # 按坐标进行裁切
    cropped = img[y0:y1, x0:x1]
    # 压缩图像尺寸到 500px
    if img.shape[1] > 500:
        resize_ratio = 500/img.shape[1]
    else:
        resize_ratio = 1.0
    resized = cv2.resize(cropped, None, fx=resize_ratio,
                         fy=resize_ratio, interpolation=cv2.INTER_AREA)
    cv2.imwrite(image, resized)


def realtime_search(image: str):
    request_url = "https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/search"
    # 二进制方式打开图片文件
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    request_url = request_url + "?access_token=" + ACCESS_TOKEN
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())


image = "./CleanShot 2021-02-25 at 18.04.20.png"
response = object_detect(image)
crop_image(image, response)
realtime_search(image)
