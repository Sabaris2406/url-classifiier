import gradio as gr
import pandas as pd
import joblib
import json
import os

# Import custom class
from feature_extraction import NIDSFeaturePreprocessor

# Load artifacts
model = joblib.load('nids_xgb_model.pkl')
preprocessor = joblib.load('feature_extractor.pkl')

EXPECTED_COLS = [
    'srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes',
    'sttl', 'dttl', 'sloss', 'dloss', 'service', 'sload', 'dload', 'spkts', 'dpkts',
    'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len',
    'sjit', 'djit', 'stime', 'ltime', 'sintpkt', 'dintpkt', 'tcprtt', 'synack', 'ackdat',
    'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd',
    'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm',
    'ct_dst_sport_ltm', 'ct_dst_src_ltm'
]

def predict_threat(json_text):
    try:
        flow_data = json.loads(json_text)
        target_url = flow_data.pop('target_url', 'Unknown URL')

        df_flow = pd.DataFrame([flow_data])
        df_flow = df_flow[EXPECTED_COLS]

        X_infer = preprocessor.transform(df_flow)
        prediction = int(model.predict(X_infer)[0])
        confidence = float(model.predict_proba(X_infer)[0][prediction] * 100)

        return {
            "target_url": target_url,
            "status": "Malicious" if prediction == 1 else "Normal",
            "confidence_percent": round(confidence, 2)
        }
    except Exception as e:
        return {"error": str(e)}

# Build the Gradio App with JSON output
demo = gr.Interface(
    fn=predict_threat,
    inputs=gr.Textbox(lines=10, label="Paste Postman JSON Payload Here"),
    outputs=gr.JSON(label="API Response"),
    title="NIDS Classification API"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
