# 虚拟画笔系统

![虚拟画笔系统示意图](https://via.placeholder.com/600x400.png?text=Virtual+Brush+System+Demo)

## 项目概述
这是一个基于计算机视觉的交互式虚拟画笔系统，结合摄像头输入和颜色检测技术，实现以下功能：
- 实时颜色检测与跟踪
- 多颜色画笔支持（蓝/绿/黄）
- 动态HSV参数调节
- 画布实时绘制与清空

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
```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装依赖
pip install opencv-python numpy gradio
