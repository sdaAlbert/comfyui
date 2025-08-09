# 在线平台安装指南

本指南适用于在liblib.ai、Runpod、Colab等线上ComfyUI平台安装mesh节点。

## 方法一：通过ComfyUI Manager（推荐）

### 1. 安装ComfyUI Manager
如果平台未预装，先安装ComfyUI Manager：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

### 2. 添加自定义节点仓库
在ComfyUI界面中：
1. 点击`Manager`按钮
2. 选择`Install via Git URL`
3. 输入仓库地址：`https://github.com/sdaAlbert/comfyui.git`
4. 点击`Install`
5. 重启ComfyUI

## 方法二：手动Git克隆

```bash
# 进入ComfyUI的custom_nodes目录
cd ComfyUI/custom_nodes

# 克隆仓库
git clone https://github.com/sdaAlbert/comfyui.git comfyui-mesh-nodes

# 进入目录
cd comfyui-mesh-nodes

# 安装依赖（如果需要）
pip install -r requirements.txt

# 运行安装脚本（可选）
python install.py
```

## 方法三：手动文件上传

如果平台支持文件上传：

1. 下载仓库ZIP文件
2. 解压到`ComfyUI/custom_nodes/comfyui-mesh-nodes/`
3. 确保包含以下文件：
   - `__init__.py`
   - `nodes.py`  
   - `requirements.txt`

## 方法四：Colab/Jupyter环境

```python
import os
os.chdir('/content/ComfyUI/custom_nodes')

# 克隆仓库
!git clone https://github.com/sdaAlbert/comfyui.git comfyui-mesh-nodes

# 安装依赖
!pip install numpy torch

# 重启运行时后启动ComfyUI
```

## 验证安装

安装成功后，在ComfyUI节点菜单中应该能看到`mesh_generation`分类，包含：
- Primitive Mesh Generator
- Mesh Transform  
- Mesh Exporter

## 常见问题

### Q: 节点没有出现在菜单中
A: 确保：
1. 文件放在正确位置：`ComfyUI/custom_nodes/comfyui-mesh-nodes/`
2. 包含`__init__.py`和`nodes.py`文件
3. 重启了ComfyUI

### Q: 缺少依赖包
A: 运行：
```bash
pip install numpy>=1.19.0 torch>=1.12.0
```

### Q: 权限问题
A: 在有些平台上可能需要：
```bash
pip install --user numpy torch
```

## 平台特殊说明

### liblib.ai
- 通常支持ComfyUI Manager
- 可以直接使用Git URL安装

### Runpod
- 建议使用Git克隆方法
- 确保在正确的工作目录

### Google Colab
- 使用上述Colab方法
- 每次重启需要重新安装

## 技术支持

如遇问题，请在GitHub Issues中反馈：
https://github.com/sdaAlbert/comfyui/issues

提供以下信息：
- 使用的平台名称
- 错误信息截图
- ComfyUI版本