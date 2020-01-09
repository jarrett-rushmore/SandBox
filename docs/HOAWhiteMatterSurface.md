## Step 0 - Setup case
```bash
case=118528
```


## Step 1 - Run N4 for Bias Field Correction
```bash
cd /rfanfs/pnl-zorro/projects/R01-HarvardOxfordAtlas/SegmentationTesting/SurfaceExtractionProtocols
N4BiasFieldCorrection -d 3 -i ../../Unrelated_100fromS1200_sMRI/${case}/T1w/T1w_acpc_dc_restore.nii.gz -o ${case}_t1w_N4.nii.gz
N4BiasFieldCorrection -d 3 -i ../../Unrelated_100fromS1200_sMRI/${case}/T1w/T2w_acpc_dc_restore.nii.gz -o ${case}_t2w_N4.nii.gz
```
## Step 2 - Run Brain Masking?
```bash
nifti_atlas csv -n 15 -o ${case}_t1w_N4 -t ${case}_t1w_N4.nii.gz trainingDataT1Masks-hdr.csv
nifti_atlas csv -n 15 -o ${case}_t2w_N4 -t ${case}_t2w_N4.nii.gz trainingDataT2Masks-hdr.csv 
```
## Step 3 - Run Freesurfer
```bash
nifti_fs -t1 ${case}_t1w_N4.nii.gz -m ${case}_t2w_N4-mask.nii.gz -o ${case}_FS -n -1
```

## Step 4 - Convert White Matter Surface to Volume
```bash
* the -r is followed by the resolution, below it is 0.7mm, but this can be adjusted to fit need.
mris_fill -r 0.7 ${case}_FS/surf/lh.white ${case}_FS/mri/lh-white-label.mgz 
```

## Step 5 - Edit WM
* load orig.mgz and lh-white-label.mgz 
* Convert lh-white-label to a segmentation
* Edit in segment editor (master volume is orig)
* Export as labelmap with the same name
* Save labelmap as lh-white-label-edited.mgz in the ${case}_FS/mri/ folder 

## Step 6 - Rerun select FS steps
```bash
export OMP_NUM_THREADS=24
cd ${case}_FS
# Tesselate, smooth and fix topology of edited label map
mkdir surf/unedited
mv surf/lh.* surf/unedited/
mri_pretess mri/lh-white-label-edited.mgz 1 mri/norm.mgz mri/lh-edited-filledpretess.mgz
mri_tessellate mri/lh-edited-filledpretess.mgz 1 surf/lh.orig.nofix
mris_extract_main_component surf/lh.orig.nofix surf/lh.orig.nofix
mris_smooth -nw -seed 1234 surf/lh.orig.nofix surf/lh.smoothwm.nofix
mris_inflate -no-save-sulc surf/lh.smoothwm.nofix surf/lh.inflated.nofix
mris_sphere -q surf/lh.inflated.nofix surf/lh.qsphere.nofix
cp surf/lh.orig.nofix surf/lh.orig
cp surf/lh.inflated.nofix surf/lh.inflated
mris_fix_topology -mgz -sphere qsphere.nofix -ga ${case}_FS lh
mris_euler_number surf/lh.orig
mris_remove_intersection surf/lh.orig surf/lh.orig
mris_smooth -n 3 -nw -seed 1234 surf/lh.orig surf/lh.white
cd ..
```

## Step 6 - Pial surface
```bash
mris_make_surfaces -nowhite -noaparc -orig_white white -pial pial -T1 brain.finalsurfs ${case}_FS lh
mris_fill -c ${case}_FS/surf/lh.pial ${case}_FS/mri/lh-pial-label.mgz
cp ${case}_FS/mri/brain.finalsurfs.mgz ${case}_FS/mri/brain.finalsurfs-edited.mgz
```
### Slicer edits
* Load brain.finalsurfs.mgz as volume
* Load lh-pial-label.mgz, lh-white-label.mgz and brain.finalsurfs-edited.mgz as labelmaps
* Import lh-pial-label and lh-white-label as Segmentations
* Use the old slicer editor with brain.finalsurfs as the master volume and brain.finalsurfs-edited as teh merge volume
* Change false positives to 1, Change false negatives to a GM intensity (~80 Intensity in the head of the caudate)

```bash
mris_make_surfaces -nowhite -noaparc -orig_white white -orig_pial pial -pial pial_edited -T1 brain.finalsurfs-edited ${case}_FS lh
```


