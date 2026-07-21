# Graduated Flask Liquid Level Detection

A Flask-based web application that detects the liquid level in transparent containers using Computer Vision and the YOLOv8 object detection model. The system analyzes uploaded images or webcam input to estimate the liquid fill percentage and display the processed output.

---

## Project Overview

Traditional liquid level measurement systems rely on physical sensors, which can be expensive, require maintenance, and may not perform well in harsh industrial environments.

This project provides a non-contact, vision-based solution that detects the liquid level in transparent containers using image processing and deep learning techniques.

---

## Features

- Upload an image for liquid level detection
- Webcam image capture
- YOLOv8-based container detection
- Automatic liquid level estimation
- Liquid fill percentage calculation
- Processed output image generation
- Flask web interface

---

## Technologies Used

- Python
- Flask
- OpenCV
- YOLOv8
- HTML
- CSS
- JavaScript

---

## Project Structure

```
Graduated-Flask-Liquid-Level-Detection/
│
├── static/
├── templates/
├── yolov8_segmentation/
├── app.py
├── yolov8n.pt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Graduated_Flask_Liquid_Level_Detection.git
```

Move into the project directory

```bash
cd Graduated_Flask_Liquid_Level_Detection
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## How It Works

1. Upload an image or capture an image using the webcam.
2. The image is processed using YOLOv8 and OpenCV.
3. The container and liquid region are detected.
4. The liquid height is calculated.
5. The fill percentage is estimated.
6. The processed image and results are displayed.

---

## Applications

- Chemical Industries
- Pharmaceutical Laboratories
- Beverage Filling Systems
- Water Tank Monitoring
- Industrial Automation
- Smart Manufacturing

---

## Future Enhancements

- Real-time video detection
- IoT integration
- Cloud-based monitoring
- Improved detection accuracy
- Support for multiple containers
- Mobile application support

---

## Author

**Meshwa Soni**

B.Tech Computer Science & Engineering (Cyber Security)

GSFC University

---

## License

This project is developed for educational and research purposes.