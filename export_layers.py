#! /usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')
import inkex
import os
import subprocess
import tempfile
import shutil
import copy

def logger(msg):
    with open(os.path.join(os.path.expanduser("~"), "layer_export.log"), "a") as myfile:
        myfile.write(str(msg) + "\n")

class ExportLayer(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.fixed = False       

    def __repr__(self):
        output = ["{}:{}".format(k,v) for (k,v) in self.__dict__.iteritems()]
        return " ".join(output)

class PNGExport(inkex.Effect):
    def __init__(self):
        """init the effect library and get options from gui"""
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--path", action="store", type="string", dest="path", default="~/", help="")
        self.OptionParser.add_option('-f', '--filetype', action='store', type='string', dest='filetype', default='jpeg', help='Exported file type')
        self.OptionParser.add_option("--crop", action="store", type="inkbool", dest="crop", default=False)
        self.OptionParser.add_option("--enum", action="store", type="inkbool", dest="enum", default=False)
        self.OptionParser.add_option("--dpi", action="store", type="float", dest="dpi", default=90.0)

    def effect(self):
        output_path = os.path.expanduser(self.options.path)
        curfile = self.args[-1]
        layers = self.get_layers(curfile)


        for layer in layers:
#            logger(layer)
            if layer.fixed:
                continue

            show_layer_ids = [l.id for l in layers if l.fixed or l.id == layer.id]
            
            if not os.path.exists(os.path.join(output_path)):
                os.makedirs(os.path.join(output_path))

            with tempfile.NamedTemporaryFile() as fp_svg:
                layer_dest_svg_path = fp_svg.name
                self.export_layers(layer_dest_svg_path, show_layer_ids)

                layer_dest_path = os.path.join(output_path, layer.name)

                if self.options.filetype == "jpeg":
                    with tempfile.NamedTemporaryFile() as fp_png:
                        self.exportToPng(layer_dest_svg_path, fp_png.name)
                        self.convertPngToJpg(fp_png.name, layer_dest_path + ".jpg")
                else:
                    self.exportToPng(layer_dest_svg_path, layer_dest_path + ".png")



    def export_layers(self, dest, show):
        """
        Export selected layers of SVG to the file `dest`.
        :arg  str   dest:  path to export SVG file.
        :arg  list  hide:  layers to hide. each element is a string.
        :arg  list  show:  layers to show. each element is a string.
        """
        doc = copy.deepcopy(self.document)
        for layer in doc.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS):
            layer.attrib['style'] = 'display:none'
            id = layer.attrib["id"]
            if id in show:
                layer.attrib['style'] = 'display:inline'

        doc.write(dest)

    def get_layers(self, src):
        svg_layers = self.document.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        layers = []

        for i, layer in enumerate(svg_layers):

            label_attrib_name = "{%s}label" % layer.nsmap['inkscape']
            if label_attrib_name not in layer.attrib:
                continue

            exp_layer = ExportLayer()
            exp_layer.name = layer.attrib[label_attrib_name]
            exp_layer.id = layer.attrib["id"]

            if exp_layer.name.lower().startswith("[fixed] "):
                exp_layer.fixed = True
                exp_layer.name = exp_layer.name[8:]
            else:
                if self.options.enum:
                    exp_layer.name = "{}_{}".format(str(i).zfill(3), exp_layer.name)    

            layers.append(exp_layer)
        return layers

    def exportToPng(self, svg_path, output_path):
        area_param = '-D' if self.options.crop else 'C'
        command = ['inkscape', area_param, '-d', self.options.dpi,'-e', output_path, svg_path]
        str_command = ["{}".format(s) for s in command]
        p = subprocess.Popen(str_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

    def convertPngToJpg(self, png_path, output_path):
        command = "convert \"%s\" \"%s\"" % (png_path, output_path)
        p = subprocess.Popen(command.encode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()


def _main():
    e = PNGExport()
    e.affect()
    exit()

if __name__ == "__main__":
    _main()
