from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
import uvicorn

# Import your custom class so joblib can unpickle it
from feature_extraction import NIDSFeaturePreprocessor

# 1. Load artifacts
model = joblib.load('nids_xgb_model.pkl')
preprocessor = joblib.load('feature_extractor.pkl')

# 2. Initialize pure API (No Gradio UI)
app = FastAPI(title="NIDS Pure API")
from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
import uvicorn

# Import your custom class so joblib can unpickle it
from feature_extraction import NIDSFeaturePreprocessor

# 1. Load artifacts
model = joblib.load('nids_xgb_model.pkl')
preprocessor = joblib.load('feature_extractor.pkl')

# 2. Initialize pure API (No Gradio UI)
app = FastAPI(title="NIDS Pure API")

@app.post("/predict")
async def predict_threat(payload: dict):
    try:
        # 1. Extract the URL for the presentation
        target_url = payload.pop('target_url', 'Unknown URL')

        # 2. Format the raw JSON into a matrix
        df_flow = pd.DataFrame([payload])
        X_infer = preprocessor.transform(df_flow)
        
        # 3. AI Prediction
        prediction = int(model.predict(X_infer)[0])
        confidence = float(model.predict_proba(X_infer)[0][prediction] * 100)
        
        return {
            "target_url": target_url,
            "status": "Malicious" if prediction == 1 else "Normal",
            "confidence_percent": round(confidence, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # Hugging Face strictly listens on port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)
@app.post("/predict")
async def predict_threat(payload: dict):
    try:
        # 1. Extract the URL for the presentation
        target_url = payload.pop('target_url', 'Unknown URL')

        # 2. Format the raw JSON into a matrix
        df_flow = pd.DataFrame([payload])
        X_infer = preprocessor.transform(df_flow)
        
        # 3. AI Prediction
        prediction = int(model.predict(X_infer)[0])
        confidence = float(model.predict_proba(X_infer)[0][prediction] * 100)
        
        return {
            "target_url": target_url,
            "status": "Malicious" if prediction == 1 else "Normal",
            "confidence_percent": round(confidence, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # Hugging Face strictly listens on port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)