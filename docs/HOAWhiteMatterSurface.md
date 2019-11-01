## Step 1 - Run N4 for Bias Field Correction
```bash
N4BiasFieldCorrection -d 3 -i ../../Unrelated_100fromS1200_sMRI/118528/T1w/T1w_acpc_dc_restore.nii.gz -o 118528_t1w_N4.nii.gz
N4BiasFieldCorrection -d 3 -i ../../Unrelated_100fromS1200_sMRI/118528/T1w/T2w_acpc_dc_restore.nii.gz -o 118528_t2w_N4.nii.gz
```
## Step 2 - Run Brain Masking?
```bash
nifti_atlas csv -n 15 -o 118528_t1w_N4 -t 118528_t1w_N4.nii.gz trainingDataT1Masks-hdr.csv
nifti_atlas csv -n 15 -o 118528_t2w_N4 -t 118528_t2w_N4.nii.gz trainingDataT2Masks-hdr.csv 
```
## Step 3 - Run Freesurfer
`recon-all -subjid <SUBJID> -all -i <SUBJID_acpc_dc_restore_N4.nii.gz -hires -parallel -openmp <n_CPU>`

## Step 4 - Import White Matter Surface in Slicer
* load <lh,rh>.white
* load nu.mgz?
* Origin issue needs to be fixed

## Step 5 - Edit WM
* Convert to segmentation
* Edit in segment editor
* Export as labelmap
* Save labelmap as <SUBJID>_<rh,lh>_white_edited.nii.gz

## Step 6 - Rerun select FS steps
```bash
export OMP_NUM_THREADS=24
# Tesselate, smooth and fix topology of edited label map
mri_pretess mri/Segmentation-label_1.mgz 1 mri/norm.mgz mri/filledpretess-1.mgz
mri_tessellate mri/filledpretess-1.mgz 1 surf/lh.orig.nofix
mris_extract_main_component surf/lh.orig.nofix surf/lh.orig.nofix
mris_smooth -nw -seed 1234 surf/lh.orig.nofix surf/lh.smoothwm.nofix
mris_inflate -no-save-sulc surf/lh.smoothwm.nofix surf/lh.inflated.nofix
mris_sphere -q surf/lh.inflated.nofix surf/lh.qsphere.nofix
cp surf/lh.orig.nofix surf/lh.orig
cp surf/lh.inflated.nofix surf/lh.inflated
mris_fix_topology -mgz -sphere qsphere.nofix -ga 100408_testing lh
mris_euler_number surf/lh.orig
mris_remove_intersection surf/lh.orig surf/lh.orig
rm surf/lh.inflated
mris_smooth -n 3 -nw -seed 1234 surf/lh.orig surf/lh.smooth-edited.white
```


