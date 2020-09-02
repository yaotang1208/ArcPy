# StandAlone Version
"""
Created on Thu Apr  2 19:28:15 2020

@author: Yao Tang
"""
import arcpy
import os

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = True

## Specify workspace(Usually the folder of the .mxd file)
arcpy.env.workspace = "L:/Projects/3020/006-01/6-0 DRAWINGS AND FIGURES/6-2 GIS/GIS/shp"
## Specify the input folder of the photos
PhotosFolder = r"L:\Projects\3020\006-01\8-0 DESIGN PHASE\DATA AND INFORMATION\Task 3 Data Collection\Geotag2ndRound\MissingInShp"
## Specify the name and the path of the output layer (GeoPhotosToPoint is the name of the layer)

## Create a geodatabase
## (A database file, only one database file is needed for the project)
database_name = "Photos_YT_2.gdb"

try:
    arcpy.CreateFileGDB_management(arcpy.env.workspace, database_name)
except:
    print "File already created"
    print "program proceed"

GridFolderList = os.listdir(PhotosFolder)

print GridFolderList


photoOption = "ALL_PHOTOS"
fieldName3 = "FacilityID"
fieldName4 = "Note"

for grid in GridFolderList:
    PhotoFolderList = os.listdir(PhotosFolder +"/" + grid)
    print PhotoFolderList
    for folder in PhotoFolderList:
        inFolder = PhotosFolder +"/" + grid + "/" + folder
        outFeatures = database_name + "/" + grid + "_" + folder
        badPhotosList = outFeatures + "_NoGPS"
        arcpy.GeoTaggedPhotosToPoints_management(inFolder, outFeatures, badPhotosList, photoOption)
        inFeatures = outFeatures        
        arcpy.AddXY_management(inFeatures)
        arcpy.AddField_management(inFeatures, fieldName3, "TEXT")
        arcpy.AddField_management(inFeatures, fieldName4, "TEXT") 

