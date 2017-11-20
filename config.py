import os

__author__ = 'shrprasha'


proj_basedir = os.path.abspath(os.path.dirname(__file__))
res_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "resources"))

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
resources_rootdir = os.path.join(basedir, "resources", "cross_aa")

if not os.path.isdir(resources_rootdir):
    resources_rootdir = os.path.join(basedir, "resources", "cross-AA")

