# -*- coding: utf-8 -*-
import json
import os
import urllib
# import urlparse
import urllib.request
from pylab import *
from PIL import Image
from PCV.localdescriptors import sift
from PCV.tools import imtools
import pydot

download_path = "data"
path = "data"

imlist = imtools.get_imlist(download_path)
nbr_images = len(imlist)

featlist = [imname[:-3] + 'sift' for imname in imlist]
for i, imname in enumerate(imlist):
    sift.process_image(imname, featlist[i])

matchscores = zeros((nbr_images, nbr_images))

for i in range(nbr_images):
    for j in range(i, nbr_images):  # only compute upper triangle
        print('comparing ', imlist[i], imlist[j])
        l1, d1 = sift.read_features_from_file(featlist[i])
        l2, d2 = sift.read_features_from_file(featlist[j])
        matches = sift.match_twosided(d1, d2)
        nbr_matches = sum(matches > 0)
        print('number of matches = ', nbr_matches)
        matchscores[i, j] = nbr_matches

# copy values
for i in range(nbr_images):
    for j in range(i + 1, nbr_images):  # no need to copy diagonal
        matchscores[j, i] = matchscores[i, j]

# 可视化

threshold = 2  # min number of matches needed to create link

g = pydot.Dot(graph_type='graph')  # don't want the default directed graph

for i in range(nbr_images):
    for j in range(i + 1, nbr_images):
        if matchscores[i, j] > threshold:
            # first image in pair
            im = Image.open(imlist[i])
            im.thumbnail((200, 200))
            filename = path + str(i) + '.jpg'
            im.save(filename)  # need temporary files of the right size
            g.add_node(pydot.Node(str(i), fontcolor='transparent', shape='rectangle', image=filename))

            # second image in pair
            im = Image.open(imlist[j])
            im.thumbnail((200, 200))
            filename = path + str(j) + '.jpg'
            im.save(filename)  # need temporary files of the right size
            g.add_node(pydot.Node(str(j), fontcolor='transparent', shape='rectangle', image=filename))

            g.add_edge(pydot.Edge(str(i), str(j)))
g.write_jpg('1.png')