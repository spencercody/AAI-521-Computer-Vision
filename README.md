# AAI-521-Computer-Vision
Final Project for AAI-521

Dataset: https://www.kaggle.com/datasets/fmena14/crowd-counting

📦 Installation

Install Dependencies
Install the required libraries listed in requirements.txt:

pip install -r requirements.txt

🚀 How to Run

1. Ensure you have the app.py and requirements.txt files in the same folder.
2. You can  update the DEFAULT_MODEL_PATH variable in app.py to point to location of best.pt.
3. If no custom model is found, the app will automatically download and use the standard yolov8n.pt (COCO pre-trained) model
4. Launch the App by running the following command in your terminal streamlit run app.py
5. Access the Dashboard Streamlit will automatically open your default web browser to http://localhost:8501
6. Upload Video: Drag and drop your CCTV or event footage (MP4/AVI) into the uploader widget.
7. Tune Parameters:
    Confidence Threshold: Increase this if you see too many false detections.
    Persistence Filter: Increase this (e.g., to 30 frames) to prevent "flickering" IDs and ensure you only count people who stay in the frame for a meaningful amount of time.
8. Watch the "Total Unique Visitors" count update in real-time as the video plays.