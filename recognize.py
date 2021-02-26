import json
import base64
import requests
import argparse
from PIL import Image
from io import BytesIO


ACCESS_TOKEN = '24.9fe297a886c240b2f0fbf055c47f6330.2592000.1616837425.282335-23708795'


def object_detect(params: dict) -> dict:
    """图像主体检测识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect"
    # 二进制方式打开图片文件

    request_url = request_url + "?access_token=" + ACCESS_TOKEN
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


def crop_and_resize_image(img_base64: str, coordinate: dict):
    """裁剪图像主体
    """
    # 读取图像
    img = Image.open(BytesIO(base64.b64decode(img_base64)))
    # 主体坐标结果
    result = coordinate['result']
    # 按坐标进行裁切
    cropped = img.crop((result['left'], result['top'], result['left'] + result['width'],
                        result['top'] + result['height']))  # (left, upper, right, lower)
    # 如果尺寸大于 500px，压缩图片
    if img.size[0] > 500:
        basewidth = 500
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        resized = cropped.resize((basewidth, hsize), Image.ANTIALIAS)
    else:
        resized = cropped
    return resized, img.size


def realtime_search(image):
    """图片相似度对比
    """
    request_url = "https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/search"
    # 将 PIL IMAGE 编码为 base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img = base64.b64encode(buffered.getvalue())
    # 图片相似度对比
    params = {"image": img}
    request_url = request_url + "?access_token=" + ACCESS_TOKEN
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


def lambda_handler(image):
    with open(image, 'rb') as f:
        img = base64.b64encode(f.read())
    params = {"image": img}
    # 目标检测
    coordinate = object_detect(params)
    # 裁切和压缩图像
    img, orignal_size = crop_and_resize_image(params['image'], coordinate)
    # 相似度比对
    results = realtime_search(img)
    payloads = {
        "orignal_image_size": orignal_size,
        "image_size": img.size,
        "object_detect": coordinate['result'],
        "result_num": results['result_num'],
        "result": results['result']
    }
    return {
        'statusCode': 200,
        'body': payloads
    }


parser = argparse.ArgumentParser()
parser.add_argument('--image', help='本地图像路径')

args = parser.parse_args()
print(lambda_handler(args.image))
