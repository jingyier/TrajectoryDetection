# 虚拟画笔系统

## 项目概述
这是一个基于计算机视觉的交互式虚拟画笔系统，结合摄像头输入和颜色检测技术，实现以下功能：
- 实时颜色检测与跟踪
- 多颜色画笔支持（蓝/绿/黄）
- 动态HSV参数调节
- 画布实时绘制与清空

项目可以做什么？

通过虚拟画笔系统实现实时颜色混合演示，教师使用不同颜色的实体教具（如彩色卡片、马克笔等），系统自动识别颜色并动态展示色块混合效果，辅助讲解色彩理论（如三原色叠加、互补色生成等）。

## 技术栈
- OpenCV (计算机视觉)
- NumPy (数值计算)
- Gradio (Web界面)
- Python 3.8+

## 功能特性
1. ​**实时颜色检测**​
   - 通过HSV色彩空间识别特定颜色
   - 支持动态调节颜色阈值参数
   - 自动过滤噪声干扰

2. ​**多模式绘画**​
   - 三种预设颜色画笔（蓝/绿/黄）
   - 实时绘制轨迹跟踪
   - 自动清除1秒前的旧轨迹

3. ​**交互式界面**​
   - 分离式参数调节面板
   - 实时画布预览
   - 清空/重置功能

## 安装步骤

### 环境准备

- 创建虚拟环境（可选）
``` bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

- 安装依赖
```
pip install opencv-python numpy gradio
```


## 使用说明

- 运行程序后自动启动摄像头
- 访问 http://localhost:7860 打开Web界面
-----------
界面分为三个主要区域：

顶部：颜色参数调节面板
中部：实时画布预览
底部：控制按钮
------------


### 操作流程


​- 颜色检测调节​

选择目标颜色（蓝/绿/黄）
调节对应HSV参数（H Min/H Max/S Min/S Max/V Min/V Max）
观察实时检测效果



#### ​绘画操作​

点击"开始绘画"按钮
在摄像头画面中移动手部进行绘制
使用清空按钮重置画布



​- 参数动态调节​

实时调节HSV参数可立即看到检测效果变化
参数范围：

H (0-179)
S (0-255)
V (0-255)
