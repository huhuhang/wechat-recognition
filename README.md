## 截图中的微信聊天窗口识别

### 实现思路

先使用目标检测方法，检测截图中的窗口主体，并把窗口裁切出来。再使用图像相似度匹配算法与库里面的不同系统，不同版本微信和 QQ 截图进行对比。如果有匹配到相似度大于某个阈值的，则返回。

### 快速验证

快速验证使用了百度云提供的 [图像单主体检测](https://cloud.baidu.com/doc/IMAGERECOGNITION/s/Xk3bcxdum) 和支持自建库的 [相同图片搜索](https://cloud.baidu.com/doc/IMAGESEARCH/s/3k3bczqz8) API。快速验证仅在图库中存放了张 Mac 版微信截图，目前仅支持对 Mac 版微信的识别和检测。

### 测试方法

```bash
python recognize.py --image test_image.png 
```

返回结果：

```json
{
  "statusCode": 200,
  "body": {
    // 原始图片尺寸
    "orignal_image_size": (1920, 1077),
    // 裁切后尺寸
    "image_size": (500, 280),
    // 窗口主体坐标
    "object_detect": {
      "top": 119,
      "left": 424,
      "width": 1132,
      "height": 877
    },
    // 匹配结果数量
    "result_num": 1,
    // 匹配图像结果
    "result": [
      {
        "brief": "Mac 微信桌面版",
        "score": 0.57444251681166,
        "cont_sign": "2730424422, 3182686714"
      }
    ]
  }
}
```
