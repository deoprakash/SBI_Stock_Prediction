# Daily Model Training - Setup Guide

## Overview
This setup trains your SBI stock prediction model **daily** with the latest 10 years of data (ending yesterday), ensuring predictions stay accurate and consistent.

---

## Files Created

### 1. `train_model.py` - Training Script
- Fetches 10 years of SBIN.NS data ending yesterday
- Engineers features (MA50, MA200, Return)
- Trains LSTM model (50 epochs)
- Saves **model.h5** and **scaler.pkl** to `model/` folder

### 2. `app.py` - Inference API (Updated)
- Loads the **saved scaler** instead of re-fitting
- Uses `scaler.transform()` (not `fit_transform()`)
- Predictions now **consistent** until next training run

### 3. `run_training.bat` - Windows Batch Script
- Activates virtual environment
- Runs `train_model.py`
- Logs success/failure

---

## Initial Setup

### Step 1: Train the Model Once
Before running the API, train the model to generate `scaler.pkl`:

```powershell
cd C:\Users\deopr\.vscode\Projects\StockPricePrediction\Backend
.\myenv\Scripts\activate
python train_model.py
```

This will:
- Download 10 years of data
- Train for ~10-15 minutes
- Save `model/sbi_model.h5`
- Save `model/scaler.pkl`

### Step 2: Start the API
```powershell
python app.py
```

Now predictions will use the fixed scaler from training!

---

## Automated Daily Training

### Option A: Windows Task Scheduler (Recommended)

1. **Open Task Scheduler** (Win + R → `taskschd.msc`)

2. **Create Basic Task**
   - Name: `SBI Model Daily Training`
   - Trigger: **Daily** at 2:00 AM (after market close)

3. **Action: Start a Program**
   - Program: `C:\Users\deopr\.vscode\Projects\StockPricePrediction\Backend\run_training.bat`
   - Start in: `C:\Users\deopr\.vscode\Projects\StockPricePrediction\Backend`

4. **Settings**
   - ☑ Run whether user is logged in or not
   - ☑ Run with highest privileges

5. **Test It**
   ```powershell
   # Run the task manually to test
   schtasks /run /tn "SBI Model Daily Training"
   ```

### Option B: Manual Batch Run
Double-click `run_training.bat` to train manually anytime.

### Option C: Built-in Auto-Train Loop
You can run the training script on a fixed interval (e.g., every 24 hours) without Task Scheduler:

```powershell
cd C:\Users\deopr\.vscode\Projects\StockPricePrediction\Backend
python train_model.py --interval 24
```
Press Ctrl+C to stop the loop.

---

## Training Schedule Recommendations

| Time | Why |
|------|-----|
| **2:00 AM** | After NSE close (3:30 PM), data is finalized |
| **5:00 AM** | Before market opens (9:15 AM), fresh model ready |

---

## Monitoring Training

### Check Last Training
```powershell
cd Backend\model
dir /od  # Shows last modified files
```

### View Training Logs
Add logging to `train_model.py` by redirecting output:
```powershell
python train_model.py >> logs\training_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log 2>&1
```

---

## Advanced: PowerShell Task Scheduler Script

For more control, create `schedule_training.ps1`:

```powershell
# Run this once to schedule daily training
$action = New-ScheduledTaskAction -Execute "C:\Users\deopr\.vscode\Projects\StockPricePrediction\Backend\run_training.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "SBI_Model_Training" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Daily LSTM model training for SBI stock prediction"
```

Run it:
```powershell
powershell -ExecutionPolicy Bypass -File schedule_training.ps1
```

---

## Troubleshooting

### Model Not Found Error
```
FileNotFoundError: model/sbi_model.h5
```
**Fix:** Run `python train_model.py` first

### Scaler Not Found Error
```
⚠ Scaler not found. Run train_model.py first!
```
**Fix:** Train the model to generate `scaler.pkl`

### Import Errors
```
Import "tensorflow" could not be resolved
```
**Fix:** Ensure virtual environment is activated:
```powershell
.\myenv\Scripts\activate
pip install -r requirements.txt
```

### Training Takes Too Long
- Reduce `EPOCHS` from 50 to 20 in `train_model.py` line 17
- Reduce data from 10y to 5y (line 33)

---

## Benefits of This Setup

✅ **Consistent Predictions** - Scaler stays fixed between training runs  
✅ **Fresh Data** - Model retrains with latest 10 years daily  
✅ **Automated** - Set it and forget it with Task Scheduler  
✅ **Separate Concerns** - Training and serving are independent  
✅ **Production Ready** - No re-fitting during inference  

---

## Next Steps

1. ✅ Train model once: `python train_model.py`
2. ✅ Start API: `python app.py`
3. ✅ Schedule daily training in Task Scheduler
4. ✅ Monitor first automated run tomorrow

**Your API will now give stable predictions until the next training cycle!** 🎯
