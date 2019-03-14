# tensorflow验证码识别

1. 样本数据
2. 创建训练数据
3. 跑模型，现在全是数字
4. 预测



## 样本数据

在`src/data/captcha`下存放验证码图片，一般名字就是答案，然后需要在`src/data/captcha.json`中描写对应关系，例如

```json
{
  "3601.jpg": "3601",
  "1651.jpg": "1651",
  "3771.jpg": "3771",
  "6172.jpg": "6172",
  "7104.jpg": "7104",
  "7134.jpg": "7134",
  "8113.jpg": "8113",
  "8395.jpg": "8395"
}
```

前面是文件名，后面是答案



## 创建训练数据

运行文件`src/create_train_data.py`，这将会创建文件`src/data/captcha.npz`和和图片1~9的数字，数字在`src/data/train`，可以打开看看，切割效果不好的话需要修改，打开文件`src/img.py`，修改如下几个参数

```python
SHIFT_PIXEL = 7  # 将图像从右向左移动
BINARY_THRESH = 30  # 图像二进制阈值
LETTER_SIZE = (20, 23)  # 字母 宽, 高
```

如果图片位置非常规则，就像这种

![](https://ws2.sinaimg.cn/large/006tKfTcly1g12h31aamwj302000y3ye.jpg)

只有4个数字，每个数字位置都确定不变，可以直接将位置写死，如

```python
letter_boxs = [[[0, 7], [11, 24]], [[13, 5], [30, 30]], [[30, 5], [45, 29]], [[47, 4], [61, 28]]]
```

上面的点分别就是下图中的1、2、3、4、5、6、7、8

![](https://ws1.sinaimg.cn/large/006tKfTcly1g12h5m9i80j30fc07rjs5.jpg)



## 跑模型

这个就比较简单了，直接运行`src/train.py`，会出现模型并保存在`src/checkpoint`目录下，



## 预测

运行`src/predict.py`，传入进去的需要是一个图片对象，当然你可以直接传入图片url，但是并不能维持session状态，因为它是直接去下载图片的，`io.imread(argv, as_gray=True)`的源码实现

```python

@contextmanager
def file_or_url_context(resource_name):
    """Yield name of file from the given resource (i.e. file or url)."""
    if is_url(resource_name):
        _, ext = os.path.splitext(resource_name)
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as f:
                u = urlopen(resource_name)
                f.write(u.read())
            # f must be closed before yielding
            yield f.name
        finally:
            os.remove(f.name)
    else:
        yield resource_name
```

他这里就是先创建了一个临时文件，将图片写进去，再读取图片。如果需要维持session状态，也可以按照他这样，先创建一个临时文件，之后再删除。







