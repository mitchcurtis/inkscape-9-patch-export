# Inkscape 9-patch Export Extension

This is an Inkscape extension that exports each top-level layer in an SVG as PNG images.

Based on Johann Woelper's fork of the original extension from Jesús Espino and Xavier Julian.

## How it works
Copy `export_9_patch.inx` and `export_9_patch.inx` into Inkscape's extension directory:

- On Linux: `$HOME/.config/inkscape/extensions/`
- On Mac: `/Applications/Inkscape.app/Contents/Resources/share/inkscape/extensions/`
- On Windows: `C:\Users\<User>\AppData\Roaming\inkscape\extensions`

This extension will export each top-level layer into a PNG image whose filename is the layer's name. The exported area is the drawing (not page), i.e. the bounding box of all objects in the layer. The exported image will display all of the visible objects in the layer without margins or cropping.

Layers with a `[9] ` prefix will be exported with a `.9.png` extension. For example, `[9] button-background` will be exported as `button-background.9.png`.

There are also options to export the layer in certain high DPI variants. The resulting images will contain the DPI as a suffix; e.g. `button-background@2x.9.png`.

## Using it
To use the extension:

1. Open the extension's dialog via **Extensions > Export > Export 9-patch PNGs...**
2. Provide the path to the output directory where the images should be saved to (Inkscape's extension system does not allow file dialogs, unfortunately).
3. Choose the DPI variants that should be exported.
4. Click OK.

## 9-patch Tips

If you have an asset that doesn't have 9-patch lines on every side, it can be useful to either:

- Add an unfilled rectangle behind the entire asset, or;
- Add a 1 x 1 unfilled rectangle where necessary

This ensures that the bounds will leave the space for the missing 9-patch lines. For example:

![9-patch example](https://github.com/mitchcurtis/inkscape-9-patch-export/blob/master/doc/images/9-patch-1-pixel.png)

After being made transparent (unfilled), the 1 pixel rectangle on the bottom right corner ensures that there are one pixel gaps on the sides of the image. If the above 50 x 32 button is exported @4x, the resulting image will look like this:

![9-patch export example](https://github.com/mitchcurtis/inkscape-9-patch-export/blob/master/doc/images/button-background@4x.9.png)

At 4 times the size, the button itself will be 200 x 128, but since the 9-patch lines are included in the bounds, it becomes 208 x 136 (4 pixels top, 4 pixels bottom, etc.). The 9-patch system requires one pixel thick lines, and so these will need to be trimmed. The simplest way to trim images in bulk is to use imagemagick:

- For @2x images: `convert *@2x.9.png -shave 1x1 *@2x.9.png`
- For @3x images: `convert *@3x.9.png -shave 2x2 *@3x.9.png`
- For @4x images: `convert *@4x.9.png -shave 3x3 *@4x.9.png`

The image above will look like this once fixed:

![9-patch export fixed example](https://github.com/mitchcurtis/inkscape-9-patch-export/blob/master/doc/images/button-background@4x.9-fixed.png)

Alternatively, if you're using the assets with Qt Quick Controls 2's [Imagine Style](https://doc.qt.io/qt-5.10/qtquickcontrols2-styles.html#imagine-style), you can use the [testbench tool](https://github.com/qt/qtquickcontrols2/tree/5.10/tests/manual/testbench) to preview and fix the assets for you.
