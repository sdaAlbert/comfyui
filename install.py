#!/usr/bin/env python3
"""
ComfyUI Mesh Nodes Installation Script
For use with online ComfyUI platforms like liblib.ai
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """检查并安装依赖"""
    required_packages = [
        'numpy>=1.19.0',
        'torch>=1.12.0'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split('>=')[0]
        try:
            importlib.import_module(package_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package_name} is missing")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✓ All dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install dependencies: {e}")
            return False
    
    return True

def verify_installation():
    """验证安装"""
    try:
        from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        
        print(f"\n✓ Installation successful!")
        print(f"✓ Found {len(NODE_CLASS_MAPPINGS)} nodes:")
        for node_name, display_name in NODE_DISPLAY_NAME_MAPPINGS.items():
            print(f"  - {display_name}")
        
        return True
    except ImportError as e:
        print(f"✗ Installation failed: {e}")
        return False

def main():
    """主安装流程"""
    print("ComfyUI Mesh Nodes Installation")
    print("=" * 40)
    
    # 检查当前目录
    if not os.path.exists('nodes.py'):
        print("✗ nodes.py not found. Please run this script in the correct directory.")
        return False
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    # 验证安装
    if not verify_installation():
        return False
    
    print("\n" + "=" * 40)
    print("Installation completed successfully!")
    print("Please restart ComfyUI to use the mesh generation nodes.")
    print("Nodes will appear in the 'mesh_generation' category.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)