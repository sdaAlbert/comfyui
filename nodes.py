import torch
import numpy as np
from typing import Any, Dict, List, Tuple, Optional

class ExampleTextNode:
    """
    示例文本处理节点
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello ComfyUI!"
                }),
                "prefix": ("STRING", {
                    "multiline": False,
                    "default": "[PREFIX] "
                }),
            },
            "optional": {
                "suffix": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "process_text"
    CATEGORY = "custom_nodes"
    
    def process_text(self, text: str, prefix: str, suffix: str = "") -> Tuple[str]:
        """处理文本的主要方法"""
        processed = f"{prefix}{text}{suffix}"
        return (processed,)


class ExampleImageNode:
    """
    示例图像处理节点
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("processed_image",)
    FUNCTION = "process_image"
    CATEGORY = "custom_nodes"
    
    def process_image(self, image: torch.Tensor, strength: float) -> Tuple[torch.Tensor]:
        """处理图像的主要方法"""
        # 简单的图像增强示例
        processed_image = torch.clamp(image * strength, 0.0, 1.0)
        return (processed_image,)


class ExampleNumberNode:
    """
    示例数值处理节点
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_a": ("FLOAT", {
                    "default": 1.0,
                    "min": -999999.0,
                    "max": 999999.0,
                    "step": 0.01
                }),
                "number_b": ("FLOAT", {
                    "default": 1.0,
                    "min": -999999.0,
                    "max": 999999.0,
                    "step": 0.01
                }),
                "operation": (["add", "subtract", "multiply", "divide"], {
                    "default": "add"
                }),
            }
        }
    
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("result",)
    FUNCTION = "calculate"
    CATEGORY = "custom_nodes"
    
    def calculate(self, number_a: float, number_b: float, operation: str) -> Tuple[float]:
        """执行数学运算"""
        if operation == "add":
            result = number_a + number_b
        elif operation == "subtract":
            result = number_a - number_b
        elif operation == "multiply":
            result = number_a * number_b
        elif operation == "divide":
            if number_b == 0:
                result = 0.0
            else:
                result = number_a / number_b
        else:
            result = 0.0
        
        return (result,)


# 节点映射配置
NODE_CLASS_MAPPINGS = {
    "ExampleTextNode": ExampleTextNode,
    "ExampleImageNode": ExampleImageNode,
    "ExampleNumberNode": ExampleNumberNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExampleTextNode": "Example Text Processor",
    "ExampleImageNode": "Example Image Processor", 
    "ExampleNumberNode": "Example Math Calculator",
}