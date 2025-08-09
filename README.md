# ComfyUI Mesh Generation Nodes

This package provides powerful mesh generation and processing nodes for ComfyUI, enabling 3D geometry creation within your workflows.

## Features

- **PrimitiveMeshGenerator**: Generate basic 3D shapes (cube, sphere, cylinder, cone, plane, torus)
- **MeshTransform**: Apply transformations (rotation, scaling) to mesh vertices
- **MeshExporter**: Export meshes to standard 3D formats (OBJ, PLY)

## Installation

### Option 1: Clone to ComfyUI custom_nodes folder

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/sdaAlbert/comfyui.git comfyui-mesh-nodes
cd comfyui-mesh-nodes
pip install -r requirements.txt
```

### Option 2: Download and extract

1. Download the repository as ZIP
2. Extract to `ComfyUI/custom_nodes/comfyui-mesh-nodes/`
3. Install dependencies: `pip install -r requirements.txt`

## Usage

After installation, restart ComfyUI. The nodes will be available in the node menu under the "mesh_generation" category.

### Available Nodes

#### Primitive Mesh Generator
Generate basic 3D geometric shapes with customizable parameters.

**Inputs:**
- `shape`: Type of primitive (cube, sphere, cylinder, cone, plane, torus)
- `resolution`: Level of detail (4-128, affects sphere/cylinder/cone quality)  
- `scale`: Overall size of the mesh (0.1-10.0)
- `center_x/y/z`: Position offset for the mesh center

**Outputs:**
- `mesh_vertices`: JSON string containing vertex coordinates
- `mesh_faces`: JSON string containing face indices  
- `vertex_count`: Number of vertices in the generated mesh

**Supported Shapes:**
- **Cube**: 8-vertex box with 12 triangular faces
- **Sphere**: UV sphere with configurable resolution
- **Cylinder**: Circular cylinder with end caps
- **Cone**: Circular cone with flat base
- **Plane**: Subdivided flat surface
- **Torus**: Ring/donut shape with major and minor radius

#### Mesh Transform
Apply 3D transformations to existing mesh vertices.

**Inputs:**
- `mesh_vertices`: JSON vertex data from generator or previous transform
- `rotation_x/y/z`: Rotation angles in degrees (-360 to 360)
- `scale_x/y/z`: Per-axis scaling factors (0.1-10.0)

**Outputs:**
- `transformed_vertices`: JSON string with transformed vertex coordinates

**Features:**
- Independent scaling on X, Y, Z axes
- Euler angle rotations applied in X→Y→Z order
- Maintains original topology (face connectivity unchanged)

#### Mesh Exporter
Convert mesh data to standard 3D file formats.

**Inputs:**
- `mesh_vertices`: JSON vertex data
- `mesh_faces`: JSON face data
- `format`: Export format (obj, ply)
- `filename`: Base name for the exported file

**Outputs:**
- `file_content`: Complete file content ready for saving

**Supported Formats:**
- **OBJ**: Wavefront OBJ format with vertices and faces
- **PLY**: Stanford PLY format (ASCII mode)

## Workflow Examples

### Basic Mesh Generation
1. Add **Primitive Mesh Generator** node
2. Select desired shape and adjust parameters  
3. Connect to **Mesh Exporter** to save the result

### Mesh Transformation Pipeline
1. Generate primitive mesh
2. Connect vertices to **Mesh Transform** 
3. Adjust rotation and scaling
4. Export transformed mesh

### Multiple Shape Combination
1. Create multiple **Primitive Mesh Generator** nodes
2. Transform each mesh to different positions/scales
3. Export each transformed mesh separately

## Technical Details

### Data Format
- Vertices are stored as JSON arrays: `[[x1,y1,z1], [x2,y2,z2], ...]`
- Faces use zero-indexed vertex references: `[[v1,v2,v3], [v4,v5,v6], ...]`
- All faces are triangulated for maximum compatibility

### Coordinate System
- Standard right-handed coordinate system
- Y-up orientation (Y+ points upward)
- Face winding follows counter-clockwise convention

### Performance Notes
- Higher resolution values increase vertex count exponentially
- Sphere: ~(resolution+1) × resolution vertices
- Torus/Cylinder: resolution² vertices
- Recommended resolution range: 8-32 for real-time use

## Development

To extend these nodes:

1. Edit `nodes.py` to add new node classes
2. Follow the existing pattern for INPUT_TYPES and RETURN_TYPES
3. Update `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`
4. Use NumPy for efficient mesh operations

### Adding New Primitives
To add a new primitive shape to PrimitiveMeshGenerator:
1. Add shape name to the `shape` input options
2. Implement `_generate_[shape]` method
3. Add case to the `generate_mesh` method

## Requirements

- Python 3.8+
- NumPy 1.19.0+ (for mesh calculations)
- PyTorch 1.12.0+ (ComfyUI dependency)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes with various mesh configurations
4. Submit a pull request

## Support

For issues, feature requests, and questions:
- GitHub Issues: https://github.com/sdaAlbert/comfyui/issues
- Include mesh parameters and error messages when reporting bugs