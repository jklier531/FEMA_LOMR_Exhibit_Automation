#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Created By: John Klier
# Created On: 08/05/2021
# Last Updated: 01/19/2022

# This is the first script in a series that has been designed to automate map production for FEMA (C)LOMR exhibits and data deliverables. Initially, this script converts existing NFHL shapefile data to usable format. From there data
# is clipped to the respective FIRM panel and imported to a file geodatabase for ease of editing. From there a FEMA schematized file geodatabse is setup and CAD2SHP shapefiles are clipped accordingly and imported to the FEMA standard
# GDB. All files are added to the APRX 'Map' and zoomed to the LOMR box at a 1:6000 scale.
#
#To do / nice to have -
#   1) Would be nice to not have to have user input GDB paths and instead setup an empty project GDB and a FEMA schmeatized GDB
#   2) Need to figure out how to make script recognize / update current map when there are multiple panels
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import system modules
import arcpy

ProjectGDB = arcpy.GetParameterAsText(0)
NFHL_Data = arcpy.GetParameterAsText(1)

aprx = arcpy.mp.ArcGISProject("CURRENT")
# Need to figure out if user input for Map name would allow the tool to switch between multiple maps in a given project. As it stands the map index defaults to the first map and only adds data to it requiring the user to copy
# features over to the additional map. Thinking a varable 'Current_Map_Name' -> arcpy.GetParameterAsText(), and call to said varaiable in the aprx.listMaps(Current_Map_Name) would work.
aprxMap = aprx.listMaps()[0]

########################################################################################################################DATA CONFIG##########################################################################
arcpy.env.workspace = ProjectGDB
arcpy.env.overwriteOutput = True

S_POL_AR_in = NFHL_Data + "/S_POL_AR.shp"
S_POL_AR_out = NFHL_Data + "/S_POL_AR_ln.shp"
S_LOMR_in = NFHL_Data + "/S_LOMR.shp"
S_LOMR_out = NFHL_Data + "/S_LOMR_ln.shp"
S_FIRM_PAN_in = NFHL_Data + "/S_FIRM_PAN.shp"
S_FIRM_PAN_number = arcpy.GetParameterAsText(2)
S_FIRM_PAN_out = ProjectGDB + "/S_FIRM_PAN_clip"
S_FIRM_PAN_clause = '"PANEL" = ' + "'%s'" %S_FIRM_PAN_number
S_FIRM_PAN_clip = arcpy.Select_analysis(S_FIRM_PAN_in, S_FIRM_PAN_out, S_FIRM_PAN_clause)

#Convert S_POL_AR to line
arcpy.FeatureToLine_management(S_POL_AR_in,S_POL_AR_out,"","ATTRIBUTES")

#Convert S_LOMR to line
arcpy.FeatureToLine_management(S_LOMR_in,S_LOMR_out,"","ATTRIBUTES")

#Set workspace to NFHL Data folder
arcpy.env.workspace = NFHL_Data

#Iterate NFHL_Data folder and clip relevant files to project GDB

S_BFE_NFHL = NFHL_Data + "\S_BFE.shp"
S_FLD_HAZ_AR_NFHL = NFHL_Data + "\S_FLD_HAZ_AR.shp"
S_FLD_HAZ_LN_NFHL = NFHL_Data + "\S_FLD_HAZ_LN.shp"
S_GEN_STRUCT_NFHL = NFHL_Data + "\S_GEN_STRUCT.shp"
S_LEVEE_NFHL = NFHL_Data + "\S_LEVEE.shp"
S_LOMR_NFHL = NFHL_Data + "\S_LOMR_ln.shp"
S_PLSS_AR_NFHL = NFHL_Data + "\S_PLSS_AR.shp"
S_POL_AR_NFHL = NFHL_Data + "\S_POL_AR_ln.shp"
S_PROFIL_BASLN_NFHL = NFHL_Data + "\S_PROFIL_BASLN.shp"
S_WTR_LN_NFHL = NFHL_Data + "\S_WTR_LN.shp"
S_XS_NFHL = NFHL_Data + "\S_XS.shp"

#if / else statements to determine if a prior run populated the project GDB with NFHL data. Deletes if so and clips applicable files into GDB feature classes.
if arcpy.Exists(ProjectGDB + "/S_BFE_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_BFE_clip")
    arcpy.Clip_analysis(S_BFE_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_BFE_clip")
else:
    arcpy.Clip_analysis(S_BFE_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_BFE_clip")

if arcpy.Exists(ProjectGDB + "/S_FLD_HAZ_AR_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_FLD_HAZ_AR_clip")
    arcpy.Clip_analysis(S_FLD_HAZ_AR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_FLD_HAZ_AR_clip")
else:
    arcpy.Clip_analysis(S_FLD_HAZ_AR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_FLD_HAZ_AR_clip")
    
if arcpy.Exists(ProjectGDB + "/S_FLD_HAZ_LN_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_FLD_HAZ_LN_clip")
    arcpy.Clip_analysis(S_FLD_HAZ_LN_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_FLD_HAZ_LN_clip")
else:
    arcpy.Clip_analysis(S_FLD_HAZ_LN_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_FLD_HAZ_LN_clip")
    
if arcpy.Exists(ProjectGDB + "/S_GEN_STRUCT_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_GEN_STRUCT_clip")
    arcpy.Clip_analysis(S_GEN_STRUCT_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_GEN_STRUCT_clip")
else:
    arcpy.Clip_analysis(S_GEN_STRUCT_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_GEN_STRUCT_clip")
    
if arcpy.Exists(ProjectGDB + "/S_LEVEE_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_LEVEE_clip")
    arcpy.Clip_analysis(S_LEVEE_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_LEVEE_clip")
else:
    arcpy.Clip_analysis(S_LEVEE_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_LEVEE_clip")
    
if arcpy.Exists(ProjectGDB + "/S_LOMR_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_LOMR_clip")
    arcpy.Clip_analysis(S_LOMR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_LOMR_clip")
else:
    arcpy.Clip_analysis(S_LOMR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_LOMR_clip")
    
if arcpy.Exists(ProjectGDB + "/S_PLSS_AR_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_PLSS_AR_clip")
    arcpy.Clip_analysis(S_PLSS_AR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_PLSS_AR_clip")
else:
    arcpy.Clip_analysis(S_PLSS_AR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_PLSS_AR_clip")
    
if arcpy.Exists(ProjectGDB + "/S_POL_AR_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_POL_AR_clip")
    arcpy.Clip_analysis(S_POL_AR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_POL_AR_clip")
else:
    arcpy.Clip_analysis(S_POL_AR_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_POL_AR_clip")
    
if arcpy.Exists(ProjectGDB + "/S_PROFIL_BASLN_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_PROFIL_BASLN_clip")
    arcpy.Clip_analysis(S_PROFIL_BASLN_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_PROFIL_BASLN_clip")
else:
    arcpy.Clip_analysis(S_PROFIL_BASLN_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_PROFIL_BASLN_clip")
    
if arcpy.Exists(ProjectGDB + "/S_WTR_LN_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_WTR_LN_clip")
    arcpy.Clip_analysis(S_WTR_LN_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_WTR_LN_clip")
else:
    arcpy.Clip_analysis(S_WTR_LN_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_WTR_LN_clip")
    
if arcpy.Exists(ProjectGDB + "/S_XS_clip"):
    arcpy.DeleteFeatures_management(ProjectGDB + "/S_XS_clip")
    arcpy.Clip_analysis(S_XS_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_XS_clip")
else:
    arcpy.Clip_analysis(S_XS_NFHL,S_FIRM_PAN_clip,ProjectGDB + "/S_XS_clip")
        
#Delete any empty Feature Classes

arcpy.env.workspace = ProjectGDB
arcpy.env.overwriteOutput = True

PGDBFCs = arcpy.ListFeatureClasses("*")

for efc in PGDBFCs:
    count1 = str(arcpy.GetCount_management(efc))
    if count1 == "0":
        arcpy.Delete_management(efc)
          
########################################################################################################################MAP SETUP############################################################################

# Set NFHL clip feature class variables
S_BFE = (ProjectGDB + "/S_BFE_clip")
S_FIRM_PAN = (ProjectGDB + "/S_FIRM_PAN_clip")
S_FLD_HAZ_AR = (ProjectGDB + "/S_FLD_HAZ_AR_clip")
S_FLD_HAZ_LN = (ProjectGDB + "/S_FLD_HAZ_LN_clip")
S_GEN_STRUCT = (ProjectGDB + "/S_GEN_STRUCT_clip")
S_LOMR = (ProjectGDB + "/S_LOMR_clip")
S_PLSS_AR = (ProjectGDB + "/S_PLSS_AR_clip")
S_POL_AR = (ProjectGDB + "/S_POL_AR_clip")
S_PROFIL_BASLN = (ProjectGDB + "/S_PROFIL_BASLN_clip")
S_WTR_LN = (ProjectGDB + "/S_WTR_LN_clip")
S_XS = (ProjectGDB + "/S_XS_clip")

# Define NFHL Clip Group Layer
NFHL_Clip_GL = aprxMap.listLayers("NFHL_Clip")[0]

if arcpy.Exists(S_FIRM_PAN):
    S_FIRM_PAN_clip = aprxMap.addDataFromPath(S_FIRM_PAN)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_FIRM_PAN_clip, "TOP")
    aprxMap.removeLayer(S_FIRM_PAN_clip)
    
if arcpy.Exists(S_FLD_HAZ_AR):
    S_FLD_HAZ_AR_clip = aprxMap.addDataFromPath(S_FLD_HAZ_AR)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_FLD_HAZ_AR_clip, "TOP")
    aprxMap.removeLayer(S_FLD_HAZ_AR_clip)
    
if arcpy.Exists(S_FLD_HAZ_LN):
    S_FLD_HAZ_LN_clip = aprxMap.addDataFromPath(S_FLD_HAZ_LN)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_FLD_HAZ_LN_clip, "TOP")
    aprxMap.removeLayer(S_FLD_HAZ_LN_clip)
    
if arcpy.Exists(S_PLSS_AR):
    S_PLSS_AR_clip = aprxMap.addDataFromPath(S_PLSS_AR)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_PLSS_AR_clip, "TOP")
    aprxMap.removeLayer(S_PLSS_AR_clip)
    
if arcpy.Exists(S_POL_AR):
    S_POL_AR_clip = aprxMap.addDataFromPath(S_POL_AR)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_POL_AR_clip, "TOP")
    aprxMap.removeLayer(S_POL_AR_clip)
    
if arcpy.Exists(S_WTR_LN):
    S_WTR_LN_clip = aprxMap.addDataFromPath(S_WTR_LN)    
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_WTR_LN_clip, "TOP")
    aprxMap.removeLayer(S_WTR_LN_clip)
    
if arcpy.Exists(S_PROFIL_BASLN):
    S_PROFIL_BASLN_clip = aprxMap.addDataFromPath(S_PROFIL_BASLN)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_PROFIL_BASLN_clip, "TOP")
    aprxMap.removeLayer(S_PROFIL_BASLN_clip)
    
if arcpy.Exists(S_GEN_STRUCT):
    S_GEN_STRUCT_clip = aprxMap.addDataFromPath(S_GEN_STRUCT)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_GEN_STRUCT_clip, "TOP")
    aprxMap.removeLayer(S_GEN_STRUCT_clip)
    
if arcpy.Exists(S_BFE):
    S_BFE_clip = aprxMap.addDataFromPath(S_BFE)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_BFE_clip, "TOP")
    aprxMap.removeLayer(S_BFE_clip)
    
if arcpy.Exists(S_XS):
    S_XS_clip = aprxMap.addDataFromPath(S_XS)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_XS_clip, "TOP")
    aprxMap.removeLayer(S_XS_clip)

if arcpy.Exists(S_LOMR):
    S_LOMR_clip = aprxMap.addDataFromPath(S_LOMR)
    aprxMap.addLayerToGroup(NFHL_Clip_GL, S_LOMR_clip, "TOP")
    aprxMap.removeLayer(S_LOMR_clip)

#Set CAD2SHP Variables
CAD2SHP_GDB = arcpy.GetParameterAsText(3)
arcpy.env.workspace = CAD2SHP_GDB
arcpy.env.overwriteOutput = True

rev_s_fld_haz_ar = arcpy.GetParameterAsText(4)
rev_s_fld_haz_ar_clip = arcpy.Clip_analysis(rev_s_fld_haz_ar,S_FIRM_PAN_out,CAD2SHP_GDB + "/rev_s_fld_haz_ar")
rev_s_fld_haz_ln = arcpy.GetParameterAsText(5)
rev_s_fld_haz_ln_clip = arcpy.Clip_analysis(rev_s_fld_haz_ln,S_FIRM_PAN_out,CAD2SHP_GDB + "/rev_s_fld_haz_ln")
rev_s_gen_struct = arcpy.GetParameterAsText(6)
rev_s_gen_struct_clip = arcpy.Clip_analysis(rev_s_gen_struct,S_FIRM_PAN_out,CAD2SHP_GDB + "/rev_s_gen_struct")
rev_s_profil_basln = arcpy.GetParameterAsText(7)
rev_s_profil_basln_clip = arcpy.Clip_analysis(rev_s_profil_basln,S_FIRM_PAN_out,CAD2SHP_GDB + "/rev_s_profil_basln")
rev_s_xs = arcpy.GetParameterAsText(8)
rev_s_xs_clip = arcpy.Clip_analysis(rev_s_xs,S_FIRM_PAN_out,CAD2SHP_GDB + "/rev_s_xs")
rev_s_LOMR = arcpy.GetParameterAsText(9)
rev_s_LOMR_clip = arcpy.Clip_analysis(rev_s_LOMR,S_FIRM_PAN_out,CAD2SHP_GDB + "/rev_s_LOMR")
rev_S_LOMR_ln = arcpy.FeatureToLine_management(rev_s_LOMR_clip,"rev_S_LOMR_ln","","ATTRIBUTES")
        

#Delete any features present in CAD2SHP feature classes and append CAD2SHP shapefiles to empty FEMA Schema GDB
CAD2SHP_Out = CAD2SHP_GDB + "/FIRM_Spatial_Layers"

arcpy.DeleteFeatures_management(CAD2SHP_Out + "/S_Fld_Haz_Ar")
C2S_s_fld_haz_ar = arcpy.Append_management(rev_s_fld_haz_ar_clip,CAD2SHP_Out + "/S_Fld_Haz_Ar","NO_TEST","","")
arcpy.DeleteFeatures_management(CAD2SHP_Out + "/S_Fld_Haz_Ln")
C2S_s_fld_haz_ln = arcpy.Append_management(rev_s_fld_haz_ln_clip,CAD2SHP_Out + "/S_Fld_Haz_Ln","NO_TEST","","")
arcpy.DeleteFeatures_management(CAD2SHP_Out + "/S_Gen_Struct")
C2S_s_gen_struct = arcpy.Append_management(rev_s_gen_struct_clip,CAD2SHP_Out + "/S_Gen_Struct","NO_TEST","","")
arcpy.DeleteFeatures_management(CAD2SHP_Out + "/S_Profil_Basln")
C2S_s_profil_basln = arcpy.Append_management(rev_s_profil_basln_clip,CAD2SHP_Out + "/S_Profil_Basln","NO_TEST","","")
arcpy.DeleteFeatures_management(CAD2SHP_Out + "/S_XS")
C2S_s_XS = arcpy.Append_management(rev_s_xs_clip,CAD2SHP_Out + "/S_XS","NO_TEST","","")
arcpy.DeleteFeatures_management(CAD2SHP_Out + "/S_LOMR")
C2S_s_LOMR = arcpy.Append_management(rev_s_LOMR_clip,CAD2SHP_Out + "/S_LOMR","NO_TEST","","")

#Create Layers for CAD2SHP
rev_s_fld_haz_ar_ly = aprxMap.addDataFromPath(C2S_s_fld_haz_ar)
rev_s_fld_haz_ln_ly = aprxMap.addDataFromPath(C2S_s_fld_haz_ln)
rev_s_gen_struct_ly = aprxMap.addDataFromPath(C2S_s_gen_struct)
rev_s_profil_basln_ly = aprxMap.addDataFromPath(C2S_s_profil_basln)
rev_s_xs_ly = aprxMap.addDataFromPath(C2S_s_XS)
rev_s_LOMR_ly = aprxMap.addDataFromPath(rev_S_LOMR_ln) 


#Define CAD2SHP Group Layer 
CAD2SHP_GL = aprxMap.listLayers("CAD2SHP")[0]


#Add CAD2SHP features to group layer
aprxMap.addLayerToGroup(CAD2SHP_GL, rev_s_fld_haz_ar_ly, "TOP")

aprxMap.addLayerToGroup(CAD2SHP_GL, rev_s_fld_haz_ln_ly, "TOP")

aprxMap.addLayerToGroup(CAD2SHP_GL, rev_s_profil_basln_ly, "TOP")

aprxMap.addLayerToGroup(CAD2SHP_GL, rev_s_gen_struct_ly, "TOP")

aprxMap.addLayerToGroup(CAD2SHP_GL, rev_s_xs_ly, "TOP")

aprxMap.addLayerToGroup(CAD2SHP_GL, rev_s_LOMR_ly, "TOP")


#Remove extra CAD2SHP layers
aprxMap.removeLayer(rev_s_LOMR_ly)
aprxMap.removeLayer(rev_s_xs_ly)
aprxMap.removeLayer(rev_s_gen_struct_ly)
aprxMap.removeLayer(rev_s_profil_basln_ly)
aprxMap.removeLayer(rev_s_fld_haz_ln_ly)
aprxMap.removeLayer(rev_s_fld_haz_ar_ly)

#Zoom Map Frame to CAD2SHP S_LOMR and set scale to 1:6000
mapObject = aprx.listMaps("Map")[0]
mapView = aprx.activeView

S_LOMR_zoom = mapObject.listLayers("S_LOMR_NFHL")[0]

mapView.panToExtent(mapView.getLayerExtent(S_LOMR_zoom, True))
mapView.camera.scale = 6000


















