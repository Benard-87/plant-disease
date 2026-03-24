# Fix for Training Error - Nested Subdirectories

## Problem
Training fails because it tries to load images from nested subdirectories that don't exist:
- `Blueberry___healthy/plant diseases names/plantvillage dataset/segmented/...`

## Solution

**Option 1: Manual Deletion (Recommended)**
1. Open File Explorer
2. Navigate to: `data\PlantVillage\Blueberry___healthy\`
3. Delete the folder: `plant diseases names`
4. If there are other nested folders in other disease folders, delete them too
5. Then run training again

**Option 2: Use Robust Training Script**
Run the robust training script which handles errors better:
```powershell
python train_robust.py --epochs 10 --batch_size 16
```

**Option 3: If OneDrive is Locking Files**
1. Pause OneDrive sync temporarily
2. Delete the nested folders manually
3. Resume OneDrive sync
4. Run training

## Quick Fix Command

After manually deleting the nested folder, run:
```powershell
python train_robust.py --epochs 10 --batch_size 16
```

The robust script will:
- Clean up any remaining nested folders
- Skip invalid file paths
- Continue training even if some files are missing

