import glob

theApp.EvtMax=100

if not "FilesInput" in dir():
    FilesInput = glob.glob("/eos/home-y/yabulait/Trigger/mc15_14TeV/mc15_14TeV.800290.*/*.pool.root.1")
#files = glob.glob("/eos/home-y/yabulait/Trigger/mc15_14TeV/mc15_14TeV.600012.*/*.pool.root.1")


tuple_name = "cells_cls.root"

include("phaseII_candc_config.py")
