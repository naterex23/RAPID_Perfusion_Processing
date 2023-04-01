### the following code requries a Slicer Kernel
### for more info check out: https://github.com/Slicer/SlicerJupyter
### Note: this code is not executable as is - feel free to email me if you would like more in depth examples / source code

import pandas as pd
import os
from pydicom import dcmread 
import nibabel as nib 
import numpy as np
import matplotlib.pyplot as plt
import nrrd
import matplotlib
import warnings
warnings.filterwarnings('ignore')
import SimpleITK as sitk
import slicer 
import SegmentStatistics

def export_seg_volume(filename):
    output_df = pd.DataFrame()
    
    #lesion_volume_node = slicer.util.loadLabelVolume(filename)
    seg = slicer.util.loadSegmentation(filename)
    #seg = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')
    #slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(lesion_volume_node, seg)
    #seg.CreateClosedSurfaceRepresentation()
    
    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", seg.GetID())
    segStatLogic.computeStatistics()
    stats = segStatLogic.getStatistics()

    if True:
        for segmentID in stats['SegmentIDs'][0:4]:
            volume_cm = np.array(stats[segmentID,"LabelmapSegmentStatisticsPlugin.volume_cm3"])
            voxel_count = np.array(stats[segmentID,"LabelmapSegmentStatisticsPlugin.voxel_count"])
            #centroid = np.array(stats[segmentID,"LabelmapSegmentStatisticsPlugin.centroid_ras"])
            output_df = output_df.append({
                                          'segment_id':segmentID,
                                          'cm_volume': volume_cm,
                                          'voxel_count': voxel_count,
                                             }, ignore_index = True)
    
    #slicer.mrmlScene.RemoveNode(lesion_volume_node)
    slicer.mrmlScene.RemoveNode(seg)   
    return output_df
print("executed this code block...")

import vtkSegmentationCorePython as vtkSegmentationCore

def extract_stats(fu_seg, rapid_seg, segmentID):
    cwd = os.getcwd()
    maskNode = slicer.util.loadLabelVolume(fu_seg)
    seg = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')
    slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(maskNode, seg, "_")
    slicer.mrmlScene.RemoveNode(maskNode)
    #maskNode2 = slicer.util.loadLabelVolume(rapid_seg)
    #seg2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')
    #slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(maskNode2, seg2, "_")
    #slicer.mrmlScene.RemoveNode(maskNode2)
    #seg = slicer.util.loadSegmentation(fu_seg)
    seg2 = slicer.util.loadSegmentation(cwd + "/" + rapid_seg)
    
    
    mergedLabelmap = vtkSegmentationCore.vtkOrientedImageData()
    seg2.GetBinaryLabelmapRepresentation(seg2.GetSegmentation().GetNthSegmentID(segmentID),mergedLabelmap)
    mergedLabelmap2 = vtkSegmentationCore.vtkOrientedImageData()
    seg.GetBinaryLabelmapRepresentation(seg.GetSegmentation().GetNthSegmentID(0),mergedLabelmap2)
    segmentationNodeNew = slicer.vtkMRMLSegmentationNode()
    slicer.mrmlScene.AddNode(segmentationNodeNew)
    segmentationNodeNew.CreateDefaultDisplayNodes()
    segmentationNodeNew.AddSegmentFromBinaryLabelmapRepresentation(mergedLabelmap,"first",[0,1,0])
    segmentationNodeNew.AddSegmentFromBinaryLabelmapRepresentation(mergedLabelmap2,"second",[0,0,1])
    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNodeNew.GetID())
    segStatLogic.computeStatistics()
    stats = segStatLogic.getStatistics()
    vols = []
    for segmentID in stats['SegmentIDs']:
        cm_volume = np.array(stats[segmentID,"LabelmapSegmentStatisticsPlugin.volume_cm3"])
        vols.append(cm_volume)
    pre_vol = vols[0]
    #print(pre_vol)
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    segmentEditorWidget.setSegmentationNode(segmentationNodeNew)
    segmentEditorWidget.setActiveEffectByName("Logical operators")
    effect = segmentEditorWidget.activeEffect()
    effect.self().scriptedEffect.setParameter("Operation","SUBTRACT")
    selectedSegmentID = effect.self().scriptedEffect.parameterSetNode().GetSelectedSegmentID()
    effect.self().scriptedEffect.setParameter("BypassMasking", 1)
    effect.self().scriptedEffect.setParameter("ModifierSegmentID",segmentationNodeNew.GetSegmentation().GetNthSegmentID(1))
    effect.self().onApply()
    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNodeNew.GetID())
    segStatLogic.computeStatistics()
    stats = segStatLogic.getStatistics()
    vols2 = []
    for segmentID in stats['SegmentIDs']:
        cm_volume = np.array(stats[segmentID,"LabelmapSegmentStatisticsPlugin.volume_cm3"])
        vols2.append(cm_volume)
        #print(segmentID, volume_cm)
    post_vol = vols2[0]
    #print(post_vol)
    overlap = pre_vol - post_vol
    #print(round(overlap,2))
    #print(overlap)
    slicer.mrmlScene.RemoveNode(seg)
    slicer.mrmlScene.RemoveNode(seg2)
    slicer.mrmlScene.RemoveNode(maskNode)
    #slicer.mrmlScene.RemoveNode(maskNode2)
    slicer.mrmlScene.RemoveNode(segmentationNodeNew)
    return(round(overlap,2))
