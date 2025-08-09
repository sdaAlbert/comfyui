# ComfyUI Custom Nodes

This package provides custom nodes for ComfyUI.

## Features

- **ExampleTextNode**: Process text with prefix and suffix
- **ExampleImageNode**: Apply strength-based image processing
- **ExampleNumberNode**: Perform basic mathematical operations

## Installation

### Option 1: Clone to ComfyUI custom_nodes folder

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/sdaAlbert/comfyui.git
cd comfyui
pip install -r requirements.txt
```

### Option 2: Download and extract

1. Download the repository as ZIP
2. Extract to `ComfyUI/custom_nodes/comfyui/`
3. Install dependencies: `pip install -r requirements.txt`

## Usage

After installation, restart ComfyUI. The nodes will be available in the node menu under the "custom_nodes" category.

### Available Nodes

#### Example Text Processor
- **Input**: Text string, prefix, optional suffix  
- **Output**: Processed text with prefix and suffix applied

#### Example Image Processor
- **Input**: Image, strength multiplier (0.0-2.0)
- **Output**: Image with brightness/intensity adjusted by strength

#### Example Math Calculator
- **Input**: Two numbers, operation (add/subtract/multiply/divide)
- **Output**: Calculated result

## Development

To modify or extend these nodes:

1. Edit `nodes.py` to add new node classes
2. Update `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`
3. Follow ComfyUI node development conventions

## Requirements

- Python 3.8+
- PyTorch 1.12.0+
- NumPy 1.19.0+
- Pillow 8.3.0+

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please use the GitHub Issues page.