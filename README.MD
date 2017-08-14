# Inkscape Export Layers

Inkscape extension to export SVG layers as (JPG, PNG) images. The exported images can be a combination of multiple layers.

Based on original extension from Jesús Espino and Xavier Julian.

It adds optional numbering and does not require a specific layer prefix. 

## How it works
place export_layers.inx and export_layers.inx into $HOME/.config/inkscape/extensions/

This extension will export each layer into a separate image file with the layer's name.

There are two options for your layers when exporting:
- **Fixed**: If a layer label starts with "[fixed]"" this layer will always be exported and combined with other layers. It is very useful for backgrounds or fixed elements.
-  Any other layer will be exported along with any [Fixed] layer and combined in a single image.

## Using it
To use the extension once your layers are ready:

1. Go to **Extensions > Export > Export layers**
2. Choose the path you want to save your file to (inkscape does not allow to use a file explorer, sorry)

3. Choose the format of your export (JPG, PNG)
