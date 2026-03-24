@echo off
echo ========================================
echo Plant Disease Model Training
echo ========================================
echo.
echo Starting training with all 40+ diseases...
echo You will see real-time progress below.
echo.
echo Press Ctrl+C to stop training
echo ========================================
echo.

python train_with_progress.py --epochs 10 --batch_size 16

echo.
echo ========================================
echo Training completed!
echo ========================================
pause

