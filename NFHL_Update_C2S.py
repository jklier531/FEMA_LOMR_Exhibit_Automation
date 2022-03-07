#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Created By: John Klier
# Created On: 08/05/2021
# Last Updated: 01/19/2022

# The is the second script in the (C)LOMR automation series that is designed to remove prelim/existing NFHL data within the Revised Area for a given case and alter S_WTR_LN / S_PROFIL_BASLN to 
# account for S_GEN_STRUCT segments.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import system modules
import arcpy

ProjectGDB = arcpy.GetParameterAsText(0)
rev_s_LOMR = arcpy.GetParameterAsText(1)
C2SGDB = arcpy.GetParameterAsText(2)

arcpy.env.workspace = ProjectGDB

S_XS = ProjectGDB + "/S_XS_clip"
S_XS_temp = "S_XS_temp"
S_BFE = ProjectGDB + "/S_BFE_clip"
S_BFE_temp = "S_BFE_temp"
S_GEN_STRUCT = ProjectGDB + "/S_GEN_STRUCT_clip"
S_GEN_STRUCT_temp = "S_GEN_STRUCT_temp"
S_GS_C2S = C2SGDB + "/FIRM_Spatial_Layers/S_Gen_Struct"
S_LOMR = ProjectGDB + "/S_LOMR_clip"
S_LOMR_out = ProjectGDB + "/S_LOMR_erase"
S_PROFIL_BASLN = ProjectGDB + "/S_PROFIL_BASLN_clip"
S_PROFIL_BASLN_out = ProjectGDB + "/S_PROFIL_BASLN_erase"
S_PBL_C2S = C2SGDB + "/FIRM_Spatial_Layers/S_Profil_Basln"
S_PBL_C2S_Out = C2SGDB + "/FIRM_Spatial_Layers/S_Profil_Basln_erase"
S_WTR_LN = ProjectGDB + "/S_WTR_LN_clip"
S_WTR_LN_out = ProjectGDB + "/S_WTR_LN_erase"
S_FLD_HAZ_LN = ProjectGDB + "/S_FLD_HAZ_LN_clip"
S_FLD_HAZ_LN_out = ProjectGDB + "/S_FLD_HAZ_LN_erase"
S_FLD_HAZ_AR = ProjectGDB + "/S_FLD_HAZ_AR_clip"
S_FLD_HAZ_AR_out = ProjectGDB + "/S_FLD_HAZ_AR_erase"

#Delete NFHL features that intersect C2S LOMR box

if arcpy.Exists(S_XS):
    arcpy.MakeFeatureLayer_management(S_XS, S_XS_temp)
    arcpy.management.SelectLayerByLocation(S_XS_temp, 'INTERSECT', rev_s_LOMR)
    arcpy.DeleteFeatures_management(S_XS_temp)
    
if arcpy.Exists(S_BFE):
    arcpy.MakeFeatureLayer_management(S_BFE, S_BFE_temp)
    arcpy.management.SelectLayerByLocation(S_BFE_temp, 'INTERSECT', rev_s_LOMR)
    arcpy.DeleteFeatures_management(S_BFE_temp)

if arcpy.Exists(S_GEN_STRUCT):
    arcpy.MakeFeatureLayer_management(S_GEN_STRUCT, S_GEN_STRUCT_temp)
    arcpy.management.SelectLayerByLocation(S_GEN_STRUCT_temp, 'WITHIN_CLEMENTINI', rev_s_LOMR)
    arcpy.DeleteFeatures_management(S_GEN_STRUCT_temp)

# Run Erase GP tool to remove sections of NFHL features present in C2S LOMR box, delete previous features from FC in project GDB, 
# append erase results to existing FC in project GDB, and delete erase results (this avoids having to add erase results to map)

if arcpy.Exists(S_LOMR):
    arcpy.Erase_analysis(S_LOMR, rev_s_LOMR, S_LOMR_out)
    arcpy.DeleteFeatures_management(S_LOMR)
    arcpy.Append_management(S_LOMR_out,S_LOMR,"NO_TEST","","")
    arcpy.Delete_management(S_LOMR_out)

if arcpy.Exists(S_PROFIL_BASLN):
    arcpy.Erase_analysis(S_PROFIL_BASLN, rev_s_LOMR, S_PROFIL_BASLN_out)
    arcpy.DeleteFeatures_management(S_PROFIL_BASLN)
    arcpy.Append_management(S_PROFIL_BASLN_out,S_PROFIL_BASLN,"NO_TEST","","")
    arcpy.Delete_management(S_PROFIL_BASLN_out)

if arcpy.Exists(S_WTR_LN):
    arcpy.Erase_analysis(S_WTR_LN, rev_s_LOMR, S_WTR_LN_out)
    arcpy.DeleteFeatures_management(S_WTR_LN)
    arcpy.Append_management(S_WTR_LN_out,S_WTR_LN,"NO_TEST","","")
    arcpy.Delete_management(S_WTR_LN_out)

if arcpy.Exists(S_FLD_HAZ_LN):
    arcpy.Erase_analysis(S_FLD_HAZ_LN, rev_s_LOMR, S_FLD_HAZ_LN_out)
    arcpy.DeleteFeatures_management(S_FLD_HAZ_LN)
    arcpy.Append_management(S_FLD_HAZ_LN_out,S_FLD_HAZ_LN,"NO_TEST","","")
    arcpy.Delete_management(S_FLD_HAZ_LN_out)

if arcpy.Exists(S_FLD_HAZ_AR):
    arcpy.Erase_analysis(S_FLD_HAZ_AR, rev_s_LOMR, S_FLD_HAZ_AR_out)
    arcpy.DeleteFeatures_management(S_FLD_HAZ_AR)
    arcpy.Append_management(S_FLD_HAZ_AR_out,S_FLD_HAZ_AR,"NO_TEST","","")
    arcpy.Delete_management(S_FLD_HAZ_AR_out)

# Change workspace to C2S GDB
arcpy.env.workspace = C2SGDB

# Run previous process on C2S GDB "S_Profil_Basln"
arcpy.Erase_analysis(S_PBL_C2S, S_GS_C2S,S_PBL_C2S_Out)
arcpy.DeleteFeatures_management(S_PBL_C2S)
arcpy.Append_management(S_PBL_C2S_Out,S_PBL_C2S,"NO_TEST","","")
arcpy.Delete_management(S_PBL_C2S_Out)



