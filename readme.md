# 高精度文本 OCR 识别

> 垂直应用场景：https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.6/applications#2
> PP-OCRv3 当文字存在下方底图、上方存在田字格或文本框时无法识别，当多个文字呈圆环形时无法识别；
> 高精度中文识别模型：https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/applications/%E9%AB%98%E7%B2%BE%E5%BA%A6%E4%B8%AD%E6%96%87%E8%AF%86%E5%88%AB%E6%A8%A1%E5%9E%8B.md
> 参考自 https://aistudio.baidu.com/aistudio/projectdetail/4436515

# 环境配置

windows 10, 不需要专门安装 cuda, cudnn

```
conda create -n paddleocr python=3.7
conda activate paddleocr

# 逐个 pip install:

paddlepaddle-gpu==2.3.2.post112  # 检查是否安装成功：paddle.utils.run_check()
shapely==1.8.4
scikit-image==0.19.3
imgaug==0.4.0
pyclipper==1.3.0
lmdb==1.3.0
tqdm==4.27.0
numpy==1.21.6
visualdl==2.3.0
rapidfuzz==2.6.0
opencv-python==4.6.0.66
opencv-contrib-python==4.6.0.66
cython==0.29
lxml==4.9.1
premailer==3.10.0
openpyxl==3.0.5
attrdict==2.0.1

Polygon3==3.0.9.1 ： Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/Could not build wheels for Polygon3, which is required to install pyproject.toml-based projects
lanms-neo==1.0.2 ： Could not build wheels for lanms-neo, which is required to install pyproject.toml-based projects

PyMuPDF<1.21.0
paddle2onnx==0.9.8
onnx==1.12.0
onnxruntime-gpu==1.12.1
```

**报错处理**：

+ Polygon3==3.0.9.1 与 lanms-neo==1.0.2 报错：Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/, Could not build wheels for Polygon3, which is required to install pyproject.toml-based projects
    - 进入 "https://visualstudio.microsoft.com/visual-cpp-build-tools/"，下载
    - 勾选："使用 C++ 的桌面开发" 下的 "MSVC v143 - VS2022 c++ x64/x86 生成工具"、"对 v143 生成工具（最新）的C++/CLI支持"、"适用于 v143 生成工具的C++模块(x64/x86)"、"Windows 10 SKD (10.0.20348.0)"、
+ Could not locate "zlibwapi.dll". Please make sure it is in your library path
    - 进入 "https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#install-zlib-windows", 下载zlib压缩包
    - 解压并将 zlibwapi.dll 放在 "C:\Windows\System32" 及 "C:\Windows\SysWOW64"



然后下载 PaddleOCR 2.6 版本: `git clone https://github.com/PaddlePaddle/PaddleOCR.git`，不需要安装



# 数据处理

将 datazip/ 文件夹下的数据解压，放到 data/ 文件夹：

```
data/
     test_images/
     train_images/
     train_lable.csv
```

`python make_data.py`


# 模型训练


`python PaddleOCR/tools/train.py -c F:\python_workspace\OCR\SVTRocr\PaddleOCR/configs/rec/PP-OCRv3/en_PP-OCRv3_rec.yml -o Global.checkpoints=F:\python_workspace\OCR\SVTRocr\output\rec\PPOCRV3_0.5\best_accuracy`


# 推理测试


`python tools/infer_rec.py -c F:\python_workspace\OCR\SVTRocr\PaddleOCR/configs/rec/PP-OCRv3/en_PP-OCRv3_rec.yml -o Global.checkpoints=F:\python_workspace\OCR\SVTRocr\output\rec\PPOCRV3_0.5\best_accuracy
`

# 导出模型转为 ONNX

```
cd ./PaddleOCR

python ./tools/export_model.py \
    -o Global.pretrained_model= F:\python_workspace\OCR\SVTRocr\output\rec\PPOCRV3_0.5\best_accuracy
    -o Global.save_inference_dir=.F:\python_workspace\OCR\SVTRocr\inference
    -c F:\python_workspace\OCR\SVTRocr\PaddleOCR/configs/rec/PP-OCRv3/en_PP-OCRv3_rec.yml

```

