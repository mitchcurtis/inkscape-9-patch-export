# Inkscape 9-patch Export Extension

This is an Inkscape extension that exports each top-level layer in a SVG as PNG images.

Based on Johann Woelper's fork of the original extension from Jesús Espino and Xavier Julian.

## How it works
Copy `export_9_patch.inx` and `export_9_patch.inx` into `$HOME/.config/inkscape/extensions/`.

This extension will export each top-level layer into a PNG image whose filename is the layer's name. The exported area is the drawing (not page), i.e. the bounding box of all objects in the layer. The exported image will display all of the visible objects in the layer without margins or cropping.

Layers with a `[9] ` prefix will be exported with a `.9.png` extension. For example, `[9] button-background` will be exported as `button-background.9.png`.

There are also options to export the layer in certain high DPI variants. The resulting images will contain the DPI as a suffix; e.g. `button-background@2x.9.png`.

## Using it
To use the extension:

1. Open the extension's dialog via **Extensions > Export > Export 9-patch PNGs...**
2. Provide the path to the output directory where the images should be saved to (Inkscape's extension system does not allow file dialogs, unfortunately).
3. Choose the DPI variants that should be exported.
4. Click OK.
