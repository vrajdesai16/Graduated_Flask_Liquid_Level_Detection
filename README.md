# Graduated Flask Liquid Level Detection

A Flask-based web application that detects the liquid level in transparent containers using Computer Vision and the YOLOv8 object detection model. The system analyzes uploaded images or webcam input to estimate the liquid fill percentage and display the processed output.

---

## Project Overview

Liquid level monitoring is essential in laboratories and industries for ensuring safety and process efficiency. Traditional sensor-based methods require physical contact and regular maintenance.

This project provides a non-contact, vision-based solution that detects the liquid level in transparent containers using image processing and deep learning techniques. The application processes images through a Flask web interface and estimates the liquid fill percentage accurately.

---

## Features

- Upload an image for liquid level detection
- Webcam image capture
- YOLOv8-based container detection
- Automatic liquid level estimation
- Liquid fill percentage calculation
- Processed output image generation
- User-friendly Flask web interface

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

## Getting Started

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Graduated_Flask_Liquid_Level_Detection.git
```

### Navigate to the project folder

```bash
cd Graduated_Flask_Liquid_Level_Detection
```

### Run the application

```bash
python app.py
```

### Open your browser

```
http://127.0.0.1:5000
```

---

## How It Works

1. Upload an image or capture an image using the webcam.
2. The image is processed using YOLOv8 and OpenCV.
3. The container and liquid region are detected.
4. The liquid height is calculated.
5. The liquid fill percentage is estimated.
6. The processed image and detection results are displayed.

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

**Vraj Desai**

B.Tech Computer Science & Engineering (Cyber Security)

GSFC University

---

## License

This project is developed for educational and research purposes.