#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 12:05:48 2018

@author: shullani
"""

import xml.etree.ElementTree as et
import pandas as pd
import numpy as np
import os
import argparse

# ONLY python 2.x
# combine badges
import svg_stack as ss


def colorStroke(svg_obj, type_data, colorHEX):
     data = svg_obj.find('.//*[@id="'+type_data+'"]')
     tmp = data.attrib['style'].replace('stroke:#000000', 'stroke:#'+colorHEX)
     data.attrib['style'] = tmp


def colorFill(svg_obj, type_data, colorHEX):
     data = svg_obj.find('.//*[@id="'+type_data+'"]')
     tmp = data.attrib['style'].replace('fill:#000000', 'fill:#'+colorHEX)
     data.attrib['style'] = tmp


def genSingleBadge(): 
    # default badge
    #svg_filepath = "./logo/drawing_2Logo.svg"
    svg_filepath = "./logo/drawing_2Logo_v3.svg"
    
    # participants list with roles
    attendants_filepath = "./attendants_list.csv"
    df_attendants = pd.read_csv(attendants_filepath, sep='|')
    
    # store SVG badge
    badges_folderpath = "./badges/"
    if not os.path.exists(badges_folderpath):
        os.mkdir(badges_folderpath)
    
    
    for idx in df_attendants.index:
        svg_obj = et.parse(open(svg_filepath))
        
        # get default attendant xml-element
        attendant_elem = svg_obj.find('.//*[@id="textAttendant"]/{http://www.w3.org/2000/svg}tspan')
        attendant_elem.text = "{} {}".format(df_attendants.loc[idx,"Firstname"], df_attendants.loc[idx,"Lastname"])
        
        # get default affiliation xml-element
        affiliation_elem = svg_obj.find('.//*[@id="textAffiliation"]/{http://www.w3.org/2000/svg}tspan')
        affiliation_elem.text = df_attendants.loc[idx,"Institution"]
        
        # get default nation xml-element
        nation_elem = svg_obj.find('.//*[@id="textNation"]/{http://www.w3.org/2000/svg}tspan')
        if isinstance(df_attendants.loc[idx,"Nation"], float):
            nation_elem.text= "*****"
        else:
            nation_elem.text = df_attendants.loc[idx,"Nation"]
    
        
        if df_attendants.loc[idx,"Type"]=="Student":
            #student all black
            colorStroke(svg_obj, "outerRect", "000000")
            colorFill(svg_obj, "mainSignal", "000000")
        elif df_attendants.loc[idx,"Type"]=="Speaker":
            #speaker all red
            colorStroke(svg_obj, "outerRect", "AA0000")
            colorFill(svg_obj, "mainSignal", "AA0000")
        elif df_attendants.loc[idx,"Type"]=="Staff":
            #staff all blue
            colorStroke(svg_obj, "outerRect", "1DB620")
            colorFill(svg_obj, "mainSignal", "1DB620")
    
        # write svg
        svg_obj.write(badges_folderpath+'badge_id_'+str(idx)+'.svg', encoding='UTF-8')






def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-genB', '--generateBadge', help='Py3.X Generate single badges from CSV file.', action="store_true", default=False)
    parser.add_argument('-combB', '--combineBadge', help='Py2.X Combine 4x2 Badges in single SVG.',  action="store_true", default=False)
    parser.add_argument('-combP', '--combinePostcard', help='Py2.X Combine Postcards in single SVG.',  action="store_true", default=False)
    return parser


if __name__ == '__main__':
    # Parse command line args
    parser = get_parser()
    args = parser.parse_args()
    if not os.path.exists("./svg_output/"):
	os.mkdir("./svg_output/")
    

    
    if args.generateBadge:
        genSingleBadge()
    elif args.combineBadge:
        ''' --------------------------------------------------------------------------------------------------- '''
        filler_badge = "./logo/drawing_2Logo_v3.svg"
        badges_folderpath = "./badges/"
        data = [os.path.join(badges_folderpath, i) for i in sorted(os.listdir(badges_folderpath))]
        
        if np.mod(len(data), 8) >0:
            for k in range(8-np.mod(len(data), 8)):
                data.append(filler_badge)
        
        
        idx_list = range(0,len(data),8)
        all_index = [range(i, i+8) for i in idx_list]
        
        
        for outer_i in range(len(all_index)):
            local_items = all_index[outer_i]
            doc = ss.Document()
            
            layout1 = ss.VBoxLayout()
            ##layout1.setSpacing(20)
            layout2 = ss.VBoxLayout()
            ##layout11.setSpacing(20)
            layout_fin = ss.HBoxLayout()
            ##layout_fin.setSpacing(20)
            
            ## column1
            for inner_i in range(4):
                local_data = data[local_items[inner_i]]
                    
                if os.path.exists(local_data):
                    layout1.addSVG(local_data,alignment=ss.AlignVCenter)

            ## column2
            for inner_i in range(4,8):
                local_data = data[local_items[inner_i]]
                    
                if os.path.exists(local_data):
                    layout2.addSVG(local_data,alignment=ss.AlignVCenter)

            layout_fin.addLayout(layout1)
            layout_fin.addLayout(layout2)
            doc.setLayout(layout_fin)
            doc.save('./svg_output/comboBadge_'+str(outer_i)+'.svg')
        ''' --------------------------------------------------------------------------------------------------- '''
    elif args.combinePostcard:
        filler_postcard = "./postcard/postcard_v2.svg"
        doc = ss.Document()
            
        layout1 = ss.VBoxLayout()
        ##layout1.setSpacing(20)
        layout2 = ss.VBoxLayout()
        ##layout11.setSpacing(20)
        layout_fin = ss.HBoxLayout()
        ##layout_fin.setSpacing(20)
        
        ## column1
        for inner_i in range(4):
            if os.path.exists(filler_postcard):
                layout1.addSVG(filler_postcard,alignment=ss.AlignVCenter)

        ## column2
        for inner_i in range(4,8):
            if os.path.exists(filler_postcard):
                layout2.addSVG(filler_postcard,alignment=ss.AlignVCenter)

        layout_fin.addLayout(layout1)
        layout_fin.addLayout(layout2)
        doc.setLayout(layout_fin)
        doc.save('./svg_output/comboPostcard_v2.svg')


        




