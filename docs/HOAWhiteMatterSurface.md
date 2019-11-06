## Step 1 - Run N4 for Bias Field Correction
```bash
cd /rfanfs/pnl-zorro/projects/R01-HarvardOxfordAtlas/SegmentationTesting/SurfaceExtractionProtocols
N4BiasFieldCorrection -d 3 -i ../../Unrelated_100fromS1200_sMRI/118528/T1w/T1w_acpc_dc_restore.nii.gz -o 118528_t1w_N4.nii.gz
N4BiasFieldCorrection -d 3 -i ../../Unrelated_100fromS1200_sMRI/118528/T1w/T2w_acpc_dc_restore.nii.gz -o 118528_t2w_N4.nii.gz
```
## Step 2 - Run Brain Masking?
```bash
nifti_atlas csv -n 15 -o 118528_t1w_N4 -t 118528_t1w_N4.nii.gz trainingDataT1Masks-hdr.csv
nifti_atlas csv -n 15 -o 118528_t2w_N4 -t 118528_t2w_N4.nii.gz trainingDataT2Masks-hdr.csv 
```
## Step 3 - Run Freesurfer
```bash
nifti_fs -t1 118528_t1w_N4.nii.gz -m 118528_t2w_N4-mask.nii.gz -o 118528_FS -n -1
```

## Step 4 - Convert White Matter Surface to Volume
```bash
mris_fill -c 118528_FS/surf/lh.white 118528_FS/mri/lh-white-label.mgz 
```

## Step 5 - Edit WM
* load orig.mgz and lh-white-label.mgz 
* Convert lh-white-label to a segmentation
* Edit in segment editor (master volume is orig)
* Export as labelmap with the same name
* Save labelmap as lh-white-label-edited.mgz in the 118528_FS/mri/ folder 

## Step 6 - Rerun select FS steps
```bash
export OMP_NUM_THREADS=24
cd 118528_FS
# Tesselate, smooth and fix topology of edited label map
mri_pretess mri/lh-white-label-edited.mgz 1 mri/norm.mgz mri/lh-edited-filledpretess.mgz
mri_tessellate mri/lh-edited-filledpretess.mgz 1 surf/lh-edited.orig.nofix
mris_extract_main_component surf/lh-edited.orig.nofix surf/lh-edited.orig.nofix
mris_smooth -nw -seed 1234 surf/lh-edited.orig.nofix surf/lh-edited.smoothwm.nofix
mris_inflate -no-save-sulc surf/lh-edited.smoothwm.nofix surf/lh-edited.inflated.nofix
mris_sphere -q surf/lh-edited.inflated.nofix surf/lh-edited.qsphere.nofix
### STOPPED HERE ###
cp surf/lh.orig.nofix surf/lh.orig
cp surf/lh.inflated.nofix surf/lh.inflated
mris_fix_topology -mgz -sphere qsphere.nofix -ga 100408_testing lh
mris_euler_number surf/lh.orig
mris_remove_intersection surf/lh.orig surf/lh.orig
rm surf/lh.inflated
mris_smooth -n 3 -nw -seed 1234 surf/lh.orig surf/lh.smooth-edited.white
```


