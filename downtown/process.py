#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
from lxml import etree
from itertools import product

from sheet_parser import load_csv, parse

BASE_MAP = os.path.dirname(__file__) + '/base_map.svg'

def export_png(svg, png):
    cmd_fmt = 'inkscape --export-png=%s --export-width=400 %s'
    cmd = cmd_fmt % (png, svg)
    print cmd
    os.system(cmd)

class DOM(object):
    def __init__(self, svg_file):
        fp = file(svg_file)
        c = fp.read()
        fp.close()
        self.dom = etree.fromstring(c)
        self.titles = [x for x in self.dom.getiterator()
                       if x.tag == '{http://www.w3.org/2000/svg}title']
        self.title_to_element = {
            t.text: t.getparent()
            for t in self.titles
        }

    def cut_element(self, title):
        e = self.title_to_element[title]
        e.getparent().remove(e)

    def add_rectangle(self, rect):
        trect = self.title_to_element['template_rect']
        group = trect.getparent()
        group.append(rect)

    def replace_text(self, title, newtext, max_chars=None):
        flowroot = self.title_to_element[title]
        flowpara = [x for x in flowroot.iterchildren() if 'flowPara' in x.tag][0]
        flowroot.remove(flowpara)
        for i, line in enumerate(newtext.split('\n')):
            paraclone = etree.fromstring(etree.tostring(flowpara))
            paraclone.text = line
            flowroot.append(paraclone)
        num_lines = i

        if max_chars and len(newtext) > (max_chars - num_lines*20):
            flowroot.attrib['style'] = re.sub(
                'font-size:\d+px;', 'font-size:8px;', flowroot.attrib['style']
            )

    def write_file(self, svg_filename):
        print svg_filename
        fp = file(svg_filename, 'w')
        fp.write(etree.tostring(self.dom))
        fp.close()

def defang(s):
    return s.replace('&','_').replace('<','_').replace('>','_')


def make_rectangle(name, i, dimensions, x, y):
    px_to_cm = 35.433
    width = dimensions[0] * px_to_cm
    height = dimensions[1] * px_to_cm
    dim_str = "%1.1fx%1.1f" % (dimensions[0], dimensions[1])
    rstr = '''
    <g>
    <rect style="fill:#ff0000;fill-opacity:0.5;stroke:none;"
       width="{w}"
       height="{h}"
       x="{x}"
       y="{y}"
       />
    <text
       style="font-size:10px;font-family:sans-serif;fill:#000000;stroke:none;"
       x="{x2}"
       y="{y2}"
       >
       <tspan x="{x3}" y="{y3}">{line1}</tspan>
       <tspan x="{x4}" y="{y4}">{line2}</tspan></text>
    </g>
    '''.format(
        w=width, h=height, x=x, y=y,
        x2=x, y2=y+13,
        x3=x, y3=y+13,
        x4=x, y4=y+26,
        line1=defang(name[:10]),
        line2=dim_str)
    print rstr
    nextx = x + width + 50
    nexty = y
    if nextx > 600:
        nextx = 0
        nexty = y + 200
    return etree.fromstring(rstr), nextx, nexty


def make_map():
    if not os.path.exists('/tmp/new_map'):
        os.makedirs('/tmp/new_map')

    csv_reader = load_csv()
    rectdata = parse(csv_reader)

    #export_png(BASE_MAP, '/tmp/new_map/back.png')

    dom = DOM(BASE_MAP)

    lastx, lasty = 0, 0

    for i, (name, dimensions) in enumerate(rectdata):

        print '\nWorking on %s %s' % ( i , name )
        print '\n'

        rect, lastx, lasty = make_rectangle(name, i, dimensions, lastx, lasty)

        dom.add_rectangle(rect)

    # Create the svg file and export a PNG
    svg_filename = '/tmp/new_map/new_map.svg'
    #png_filename = '/tmp/new_map/new_map.png'

    dom.write_file(svg_filename)

    #export_png(svg_filename, png_filename)


if __name__ == '__main__':
    make_map()
