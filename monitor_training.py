"""
Monitor training progress by checking model file updates
Run this script to periodically check if training is progressing
"""
import os
import time
import json
from datetime import datetime

def monitor_training(check_interval=60, max_checks=60):
    """
    Monitor training progress
    
    Args:
        check_interval: Seconds between checks (default 60 = 1 minute)
        max_checks: Maximum number of checks (default 60 = 1 hour)
    """
    model_path = "models/plant_disease_model.h5"
    initial_size = 0
    initial_time = None
    
    if os.path.exists(model_path):
        initial_size = os.path.getsize(model_path)
        initial_time = os.path.getmtime(model_path)
        print(f"📦 Initial model size: {initial_size / (1024*1024):.2f} MB")
        print(f"📅 Initial model time: {datetime.fromtimestamp(initial_time).strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("⚠️  Model file not found - training will create it")
    
    print(f"\n🔍 Monitoring training progress...")
    print(f"   Check interval: {check_interval} seconds")
    print(f"   Will check up to {max_checks} times ({max_checks * check_interval / 60:.1f} minutes)")
    print(f"   Press Ctrl+C to stop monitoring\n")
    print("=" * 60)
    
    for check_num in range(1, max_checks + 1):
        try:
            time.sleep(check_interval)
            
            if os.path.exists(model_path):
                current_size = os.path.getsize(model_path)
                current_time = os.path.getmtime(model_path)
                size_change = current_size - initial_size
                time_change = current_time - initial_time
                
                status = "🟢 ACTIVE" if time_change > 0 or size_change != 0 else "⏸️  IDLE"
                
                print(f"[Check {check_num}/{max_checks}] {datetime.now().strftime('%H:%M:%S')} - {status}")
                print(f"   Size: {current_size / (1024*1024):.2f} MB (change: {size_change / (1024*1024):+.2f} MB)")
                print(f"   Last modified: {datetime.fromtimestamp(current_time).strftime('%H:%M:%S')}")
                
                if time_change > 0:
                    print(f"   ✅ Model was updated! Training is progressing.")
                    initial_time = current_time
                    initial_size = current_size
                else:
                    print(f"   ⏸️  No changes detected")
            else:
                print(f"[Check {check_num}/{max_checks}] {datetime.now().strftime('%H:%M:%S')} - Model file not found yet")
            
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Error during check: {e}")
    
    print("\n✅ Monitoring complete")

if __name__ == "__main__":
    import sys
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    max_ch = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    monitor_training(check_interval=interval, max_checks=max_ch)

