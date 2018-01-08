#! /usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')
import copy
import logging
import inkex
import os
import shutil
import subprocess
import tempfile

class ExportLayer(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.fixed = False
        self.ninePatch = False

    def __repr__(self):
        output = ["{}:{}".format(k,v) for (k,v) in self.__dict__.iteritems()]
        return " ".join(output)

class PNGExport(inkex.Effect):
    def __init__(self):
        # init the effect library and get options from gui
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--dir", action="store", type="string", dest="dir", default="~/", help="")
#        self.OptionParser.add_option("--crop", action="store", type="inkbool", dest="crop", default=True)
        self.OptionParser.add_option("--basedpi", action="store", type="float", dest="basedpi", default=90.0)
        self.OptionParser.add_option("--dpi2", action="store", type="inkbool", dest="dpi2", default=False)
        self.OptionParser.add_option("--dpi3", action="store", type="inkbool", dest="dpi3", default=False)
        self.OptionParser.add_option("--dpi4", action="store", type="inkbool", dest="dpi4", default=False)

    def effect(self):
        outputDirPath = os.path.expanduser(self.options.dir)
        curfile = self.args[-1]
        layers = self.getLayers(curfile)

        for layer in layers:
            if layer.fixed:
                continue

            # TODO: if we wanted to add support for merging sub-layers into the parent,
            # we'd probably need to add the sub-layers to this list.
            showLayerIds = [l.id for l in layers if l.fixed or l.id == layer.id]
            
            # If the output directory doesn't exist, create it.
            if not os.path.exists(os.path.join(outputDirPath)):
                os.makedirs(os.path.join(outputDirPath))

            with tempfile.NamedTemporaryFile() as fpSvg:
                layerDestSvgPath = fpSvg.name
                self.exportLayers(layerDestSvgPath, showLayerIds)

                layerDestPath = os.path.join(outputDirPath, layer.name)

                self.exportToPng(layerDestSvgPath, layerDestPath, layer.ninePatch)



    def exportLayers(self, dest, show):
        # Export selected layers of SVG to the file `dest`.
        # :arg  str   dest:  path to export SVG file.
        # :arg  list  hide:  layers to hide. each element is a string.
        # :arg  list  show:  layers to show. each element is a string.
        doc = copy.deepcopy(self.document)
        for layer in doc.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS):
            layer.attrib['style'] = 'display:none'
            id = layer.attrib["id"]
            if id in show:
                layer.attrib['style'] = 'display:inline'

        doc.write(dest)

    def getLayers(self, src):
        svgLayers = self.document.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        layers = []

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        for i, layer in enumerate(svgLayers):
#            stuff = { "layer": layer.attrib, "i": i }
#            logger.info("Layer %s", stuff);

            labelAttribName = "{%s}label" % layer.nsmap['inkscape']
            if labelAttribName not in layer.attrib:
                continue

            expLayer = ExportLayer()
            expLayer.name = layer.attrib[labelAttribName]
            expLayer.id = layer.attrib["id"]

#            if expLayer.name.lower().startswith("[fixed] "):
#                expLayer.fixed = True
#                expLayer.name = expLayer.name[8:]

            if expLayer.name.lower().startswith("[9] "):
                expLayer.ninePatch = True
                expLayer.name = expLayer.name[4:]

            layers.append(expLayer)
        return layers

    # baseOutputPath - the path where the PNG should be saved to,
    #    without any file extension. e.g. "~/button-background"
    def exportToPng(self, svgPath, baseOutputPath, isNinePatch):
        self.exportPngAtDpiMultiplier(svgPath, baseOutputPath, 1, isNinePatch)
        if self.options.dpi2:
            self.exportPngAtDpiMultiplier(svgPath, baseOutputPath, 2, isNinePatch)
        if self.options.dpi3:
            self.exportPngAtDpiMultiplier(svgPath, baseOutputPath, 3, isNinePatch)
        if self.options.dpi4:
            self.exportPngAtDpiMultiplier(svgPath, baseOutputPath, 4, isNinePatch)

    def exportPngAtDpiMultiplier(self, svgPath, baseOutputPath, multiplier, isNinePatch):
        # Construct the path.
        outputPath = baseOutputPath
        if multiplier > 1:
            outputPath += "@" + str(multiplier) + "x"
        if isNinePatch:
            outputPath += ".9"
        outputPath += ".png"

        # If the 'Crop to bounds' option was checked, crop to the drawing.
        # Otherwise, crop to the page.
#        area_param = '-D' if self.options.crop else 'C'
        area_param = '-D'
        finalDpi = self.options.basedpi * multiplier
        command = ['inkscape', area_param, '-d', finalDpi,'-e', outputPath, svgPath]
        strCommand = ["{}".format(s) for s in command]
        p = subprocess.Popen(strCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

def _main():
    e = PNGExport()
    e.affect()
    exit()

if __name__ == "__main__":
    _main()
