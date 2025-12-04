import streamlit as st
import cv2
import tempfile
import os
from ultralytics import YOLO
from collections import defaultdict
import pandas as pd
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Crowd Analytics Pro",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Event Attendance & Crowd Analytics")
st.markdown("""
**Upload a CCTV or Event Feed** to analyze crowd density and unique attendance.
This system uses a custom-trained **YOLOv8** model with **ByteTrack** and persistence filtering.
""")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Model Settings")

# Path to your trained model
DEFAULT_MODEL_PATH = "/Users/rdhanase/USD/AAI-521/Final_Project/AAI-521-Computer-Vision/best.pt"

# Allow user to pick model if they want, else use default
model_source = st.sidebar.radio("Model Source", ["Use Project Model (best.pt)", "Use Standard YOLOv8n"])
if model_source == "Use Project Model (best.pt)":
    model_path = DEFAULT_MODEL_PATH
    if not os.path.exists(model_path):
        st.sidebar.warning(f"⚠️ '{model_path}' not found. Using 'yolov8n.pt' instead.")
        model_path = "yolov8n.pt"
else:
    model_path = "yolov8n.pt"

# Confidence Threshold
conf_thresh = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.3, 0.05)

# Persistence Filter
min_frames = st.sidebar.slider("Persistence Filter (Frames)", 1, 60, 10, 
                               help="How many frames a person must be tracked before counting them.")

# --- MAIN APP LOGIC ---

uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save uploaded file to temp so OpenCV can read it
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    # Setup Processing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st_frame = st.empty() # Placeholder for video frame
    
    with col2:
        st.subheader("Live Metrics")
        metric_curr = st.empty()
        metric_unique = st.empty()
        st.write("---")
        st.subheader("Traffic Trend")
        chart_placeholder = st.empty()

    # Load Model
    try:
        model = YOLO(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

    # Processing Loop
    cap = cv2.VideoCapture(video_path)
    
    track_history = defaultdict(int)
    verified_ids = set()
    
    # For Charting
    chart_data = pd.DataFrame(columns=['Frame', 'Density'])
    frame_count = 0
    
    # Progress Bar
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = st.progress(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame_count += 1
        
        # Run Tracking
        results = model.track(frame, persist=True, verbose=False, conf=conf_thresh, tracker="bytetrack.yaml")
        
        current_density = 0
        
        # Logic
        if results[0].boxes.id is not None:
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            current_density = len(ids)
            
            for pid in ids:
                track_history[pid] += 1
                if track_history[pid] > min_frames:
                    verified_ids.add(pid)
        
        # Visualization
        annotated_frame = results[0].plot()
        
        # Update Dashboard every few frames to save performance
        if frame_count % 3 == 0:
            # Update Metrics
            metric_curr.metric("Current Density", current_density)
            metric_unique.metric("Total Unique Visitors", len(verified_ids))
            
            # Update Chart
            new_row = pd.DataFrame({'Frame': [frame_count], 'Density': [current_density]})
            chart_data = pd.concat([chart_data, new_row], ignore_index=True)
            
            chart = alt.Chart(chart_data).mark_line().encode(
                x='Frame',
                y='Density',
                tooltip=['Frame', 'Density']
            ).properties(height=200)
            chart_placeholder.altair_chart(chart, use_container_width=True)
            
            # Update Video Frame
            # Streamlit requires RGB, OpenCV gives BGR
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            st_frame.image(frame_rgb, channels="RGB", use_column_width=True)
            
            # Update Progress
            if total_frames > 0:
                progress_bar.progress(min(frame_count / total_frames, 1.0))

    cap.release()
    st.success(f"Processing Complete! Total Unique Attendees: {len(verified_ids)}")