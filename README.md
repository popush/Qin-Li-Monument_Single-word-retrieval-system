# Qin-Li-Monument_Single-word-retrieval-system
# 《勤礼碑》单字检索系统
## 本系统是本人的毕业设计，仅供学习交流和西安理工大学计算机学院老师的查阅

摘  要
随着时代的发展，计算机视觉逐步发展成为当下计算机科学领域中热门的一个方向，书法是中华文化的精粹，历经几千年仍焕发着强大的艺术魅力。使用计算机图形图像特征识别技术处理书法字图像具有重要的研究价值。
本文使用数字图像处理的诸多算法，对汉字书法的切割以及汉字识别这两个问题进行了研究。本文的主要工作包括：
1.图像的预处理部分：主要包括了均值偏移滤波，腐蚀算法，膨胀算法，图像二值化等步骤，算法以及实现效果在本文中都有详细的介绍。预处理部分为文章后续的处理提供了良好的基础。
2.汉字切割部分主要实现了行列积分切割算法和区域扩张算法，其中行列积分切割算法对预处理后的图像进行横向以及纵向的积分，结合碑文的特点分析波谷并找出行、列切割线，该算法用于对碑文所有汉字的切割中。区域扩张法选择了一个合适的大小的矩形方盒，当盒子处于一个汉字内部时，对上下左右进行扩张，直到矩形扩张到不是字的地方，该方法用于对单个汉字的切割；
3.汉字识别部分，主要介绍图像匹配算法，LeNet、Alex Net 的优缺点。本系统最终选择Alex Net网络作为汉字识别的工具。
4.检索部分分析了顺序存储方法、链式存储方法、索引存储方法以及散列存储方法，本文系统中最终使用了散列存储方法（hash存储）以及顺序存储方法作为最终的存储结构。
5.系统实现与结果分析：本检索系统使用python设计并实现人机界面，实现对碑文汉字的切割、识别、检索等工作。
本文在PyCharm编译器上使用python语言、OpenCV视觉库、TensorFlow机器学习框架等，实现了图像的预处理、图像分割、图像识别等任务，并取得了较良好的效果。
关键词：图像处理；图像分割；图像识别；哈希存储

