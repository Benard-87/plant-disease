# How to Train the Model in Visual Studio Code

## Quick Start

1. **Open VS Code Terminal** (Ctrl + ` or View → Terminal)

2. **Run the training command:**
   ```bash
   python train_model.py --data_dir "data/PlantVillage" --epochs 50 --batch_size 32
   ```

   Or use the shorter version:
   ```bash
   py train_model.py --data_dir "data/PlantVillage" --epochs 50 --batch_size 32
   ```

## What You'll See

- Model building progress
- Training progress for each epoch
- Accuracy and loss metrics
- Model will be saved automatically when validation improves

## Training Details

- **Dataset**: 38 disease classes
- **Total Images**: ~76,659 images
- **Epochs**: 50 (may stop early if no improvement)
- **Batch Size**: 32
- **Expected Time**: 4-8 hours (depends on your system)

## After Training

The model will be saved to:
- `models/plant_disease_model.h5` - Main model file
- `models/class_indices.json` - Class mappings
- `models/training_history.png` - Training graphs

## Run the App

After training completes, run:
```bash
streamlit run app.py
```

Or:
```bash
py -m streamlit run app.py
```

## Troubleshooting

If you see errors about missing files in nested folders, run:
```bash
python cleanup_nested_folders.py
```

Then try training again.

