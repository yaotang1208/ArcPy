"""
Created on Wed Apr 8

@author: Yao Tang
This program inserts the photos from one grid to a geodatabase, add the desired fields,
and assign a Facility ID
"""
import arcpy
import pandas as pd
import numpy as np
from pandas import DataFrame
import os

arcpy.env.overwriteOutput = False
arcpy.env.addOutputsToMap = True

## Specify workspace(Usually the folder of the .mxd file)
arcpy.env.workspace = "L:/Projects/3020/006-01/6-0 DRAWINGS AND FIGURES/6-2 GIS/GIS/shp"
## Specify the Grid folder of the photos
GridFolder = "L:/Projects/3020/006-01/8-0 DESIGN PHASE/DATA AND INFORMATION/Task 3 Data Collection/Survey_20200504/Photos_JZ_20200504"
## Create a geodatabase. You may want to create a gdb file with your initials to keep track of the process. eg. YT is short for Yao Tang.
database_name = "Photos_YT_05062020.gdb"
## Specify FacilityID shapefile
feature_FID = 'L:/Projects/3020/006-01/8-0 DESIGN PHASE/DATA AND INFORMATION/Task 3 Data Collection/GIS/FacilityID_shapefile/FacilityID_WGS84.shp'

## dataframe function
def feature_class_to_pandas_data_frame(feature_class, field_list):
    """
    Load data into a Pandas Data Frame for subsequent analysis.
    :param feature_class: Input ArcGIS Feature Class.
    :param field_list: Fields for input.
    :return: Pandas DataFrame object.
    """
    return DataFrame(
        arcpy.da.FeatureClassToNumPyArray(
            in_table=feature_class,
            field_names=field_list,
            skip_nulls=False,
            null_value=-99999
        )
    )
field_list_FID = ['FID', 'FacilityID','POINT_X','POINT_Y']
df_FID = feature_class_to_pandas_data_frame(feature_FID, field_list_FID)
print "FacilityID file imported"
## end of dataframe function

try:
    arcpy.CreateFileGDB_management(arcpy.env.workspace, database_name)
    print "A new geodatabase is created"
except:
    print "File already created, program proceeds"
    #print "program proceeds"

Gridname = '_'.join(GridFolder.split('/')[-1].split())
print "Grid name is " + Gridname
PhotoFolderList = os.listdir(GridFolder)
print "Folders at this grid are :"
print(PhotoFolderList)

photoOption = "ALL_PHOTOS"
fieldName3 = "FacilityID"
fieldName4 = "Note"

for folder in PhotoFolderList:
    print "Adding photos from [" + folder + "]"
    inFolder = GridFolder + "/" + folder
    #foldername = '_'.join(folder.split('.'))
    outFeatures = database_name + "/" + Gridname + "_" + folder
    badPhotosList = outFeatures + "_NoGPS"
    try:
        arcpy.GeoTaggedPhotosToPoints_management(inFolder, outFeatures, badPhotosList, photoOption)
        inFeatures = outFeatures        
        arcpy.AddXY_management(inFeatures)
        arcpy.AddField_management(inFeatures, fieldName3, "TEXT")
        arcpy.AddField_management(inFeatures, fieldName4, "TEXT")
        
        cur = arcpy.UpdateCursor(inFeatures)

        for row in cur:
            x = row.getValue('POINT_X')
            x = x if x is not None else 0
            y = row.getValue('POINT_Y')
            y = y if y is not None else 0
            df_FID['Distance'] = [(df_FID['POINT_X'][i] - x)**2 + (df_FID['POINT_Y'][i] - y)**2 for i in range(len(df_FID))]
            ind_min = df_FID['Distance'].idxmin()
            row.setValue('FacilityID',df_FID['FacilityID'][ind_min])
            cur.updateRow(row)
    except:
        print "Feature already created or folder name has '.'. Please delete the features or change names and try again"

print "Program ended"
