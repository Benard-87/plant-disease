# How to Train the Model with Progress Display

## Quick Start

**Option 1: Double-click the batch file**
- Double-click `start_training.bat`
- This will open a window showing all training progress

**Option 2: Run in PowerShell/Command Prompt**
```powershell
python train_with_progress.py --epochs 10 --batch_size 16
```

**Option 3: Run with custom settings**
```powershell
python train_with_progress.py --epochs 20 --batch_size 32
```

## What You'll See

The training script will show:
1. **Data Loading**: Number of classes and samples found
2. **Model Building**: ResNet50 architecture setup
3. **Training Progress**: 
   - Epoch-by-epoch progress bars
   - Training accuracy and loss
   - Validation accuracy and loss
   - Real-time updates

## Training Parameters

- **--epochs**: Number of training epochs (default: 10)
  - More epochs = better accuracy but longer training
  - Recommended: 10-20 for initial training
  
- **--batch_size**: Images processed at once (default: 16)
  - Smaller = less memory, slower training
  - Larger = more memory, faster training
  - Adjust based on your RAM

## Expected Timeline

- **Data Loading**: 1-5 minutes
- **Model Building**: 1-2 minutes  
- **Training (10 epochs)**: 30 minutes to 2+ hours
  - Depends on:
    - Number of images per class
    - Your computer's CPU/GPU
    - Batch size

## Monitoring Progress

While training, you'll see output like:
```
Epoch 1/10
[=====>] 125/125 - 45s 360ms/step - loss: 2.3456 - accuracy: 0.2345
val_loss: 2.1234 - val_accuracy: 0.3456

Epoch 1 Results:
  Training - Loss: 2.3456, Accuracy: 23.45%
  Validation - Loss: 2.1234, Accuracy: 34.56%
```

## After Training

When training completes:
- ✅ Model saved to `models/plant_disease_model.h5`
- ✅ Class indices saved to `models/class_indices.json`
- ✅ Training history plot saved to `models/training_history.png`
- ✅ Training log saved to `models/training_log.csv`

## Restart Your App

After training completes:
1. Stop your Streamlit app (if running)
2. Restart it: `streamlit run app.py`
3. The new model with all 40 classes will be loaded automatically

## Troubleshooting

**If training is too slow:**
- Reduce epochs: `--epochs 5`
- Increase batch size: `--batch_size 32` (if you have enough RAM)
- Close other applications to free up resources

**If you run out of memory:**
- Reduce batch size: `--batch_size 8`
- Close other applications

**To stop training:**
- Press `Ctrl+C` in the terminal
- The best model so far will be saved automatically

