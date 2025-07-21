# Amazon Customer Reviews Sentiment Analysis

A Python-based, production-ready sentiment analysis platform for Amazon product reviews. It leverages a fine-tuned DistilBERT model for deep learning, robust preprocessing pipelines, comprehensive evaluation and visualization tools, and a FastAPI-powered interactive web interface.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview
This project delivers an end-to-end sentiment analysis solution for Amazon customer reviews, including:
- Fine-tuned DistilBERT model for 1-5 star sentiment classification
- Interactive web interface (FastAPI)
- Automated data preprocessing and cleaning
- Dockerized deployment support
- Comprehensive evaluation and visualization utilities

It is designed for researchers, developers, and organizations seeking advanced sentiment analysis capabilities and easy extensibility.

---

## Features
- **Fine-tuned DistilBERT Sentiment Model**: Accurately classifies reviews into 1-5 star ratings.
- **Automated Data Preprocessing**: Cleans, balances, and splits raw review data for optimal model performance.
- **FastAPI Web Interface**: User-friendly, interactive web app for real-time sentiment prediction.
- **Evaluation & Visualization Tools**: Generates confusion matrices, classification reports, and performance metrics.
- **Docker Support**: Seamless deployment in any environment.

---

## Installation

1. **Clone the repository:**
   ```bash
git clone https://github.com/yagmurtncr/Amazon-Customer-Reviews-Sentiment-Analysis.git
cd amazon-ratings-sentiment
```
2. **(Optional) Create a virtual environment:**
   ```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Linux/Mac
```
3. **Install dependencies:**
   ```bash
pip install -r requirements.txt
```
4. **(Optional) Run with Docker:**
   ```bash
docker-compose up --build
```

---

## Usage

### 1. Data Preparation
Generate training and test datasets from raw reviews:
```bash
python preprocess.py
```

### 2. Model Training
Train the DistilBERT sentiment analysis model:
```bash
python train_model.py
```

### 3. Model Evaluation
Evaluate the trained model and generate metrics/visualizations:
```bash
python evaluate.py
```

### 4. Launch the Web Interface
Start the FastAPI web app for interactive predictions:
```bash
uvicorn app:app --reload
```
- Open your browser at [http://localhost:8000](http://localhost:8000)
- Enter review text and view predicted sentiment.

### 5. Command-Line Model Testing
Test the model with sample inputs via the command line:
```bash
python test_model.py
```

---

## Directory Structure
- `app.py`             : FastAPI backend and web interface
- `evaluate.py`        : Model evaluation and visualization
- `train_model.py`     : Model training script
- `preprocess.py`      : Data preprocessing utilities
- `postprocess.py`     : Model inference utilities
- `amazon_data/`       : Raw and processed data files
- `final_model/`       : Trained model checkpoints
- `results/`           : Evaluation and visualization outputs
- `templates/`         : HTML templates for the web interface
- `static/`            : Static files (CSS, images)

---

## Contributing
Contributions are welcome! Please open an issue to discuss your ideas or submit a pull request for review. For major changes, start a discussion first.

---

## License
MIT License © 2025 Your Name

---

## Contact
For questions or collaboration, please contact [y.tuncer1004@gmail.com].
