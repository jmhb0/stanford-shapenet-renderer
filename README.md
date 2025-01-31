# Changes in this fork 
- For blender compatibility to 3.X (I think), changed key "View Names" to "View\_Names". 
- Changed the lighting a bit. Before there was one primary light on one side (e.g. the side of cars) and one very faint light on the other. I set them to be the same. Also lowered the power of the light from 10 to 6.
- Inside ShapeNetCore.v2, copied over `all.csv` which is a list of ShapeNet object uids, and `all_categories.txt` which is a lookup from class names to class uids. 
- Added a script `ShapeNetCore.v2/sample_files.py` to sample a subset of uids based on their class (e.g. cars), and then copy them over from a server (since Blender is not running on server for me). The script also calls the rendering script `render_blender.py`.

# Stanford Shapenet Renderer

A little helper script to render .obj files (such as from the stanford shapenet database) with Blender.

Tested on Linux, but should also work for other operating systems.
By default, this scripts generates 30 images by rotating the camera around the object.
Additionally, depth, albedo, normal and id maps are dumped for every image.

Tested with Blender 2.9

## Example invocation

To render a single `.obj` file, run

    blender --background --python render_blender.py -- --output_folder /tmp path_to_model.obj

To get raw values that are easiest for further use, use `--format OPEN_EXR`. If the .obj file references any materials defined in a `.mtl` file, it is assumed to be in the same folder with the same name.

## Batch rendering

To render a whole batch, you can e. g. use the unix tool find:

    find . -name *.obj -exec blender --background --python render_blender.py -- --output_folder /tmp {} \;

To speed up the process, you can also use xargs to have multiple blender instances run in parallel using the `-P` argument

    find . -name *.obj -print0 | xargs -0 -n1 -P3 -I {} blender --background --python render_blender.py -- --output_folder /tmp {}

## Example images

Here is one chair model rendered with 30 different views:

![Chairs](examples/out_without_specular.png)

or a teapot with all available outputs

![Teapots](examples/teapot_all_outputs.jpg)


