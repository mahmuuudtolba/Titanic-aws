# Titanic Survival Prediction 🚢

This is an implementation of a machine learning classification model for predicting Titanic passenger survival.

## Requirements
- Python 3.11 or later

## Installation 

### Using Anaconda
```bash
conda create --prefix ./venv python=3.11 -y
conda activate ./venv
```

### Using pip
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Testing

### Run simple tests
```bash
python run_simple_tests.py
```

### Run specific tests
```bash
# Run all simple tests
pytest tests/test_simple.py -v

```

### See available tests
```bash
python run_simple_tests.py --list
```

For a complete testing guide, see [TESTING_GUIDE.md](TESTING_GUIDE.md)

## Usage

### Run the ML pipeline
```bash
python pipeline/training_pipeline.py
```

### Launch the Flask application
```bash
python application.py
```

The application will be available at `http://localhost:5000`

## Docker

### Build the image
```bash
docker build -t titanic-image .
```

### Run the container
```bash
docker run --name titanic-container -p 5000:5000 -v ./.aws:/root/.aws:ro titanic-image
```

## Project Structure

```
├── src/                    # Source code
│   ├── data_ingestion.py  # Data loading from AWS S3
│   ├── data_processing.py # Data preprocessing and feature engineering
│   └── model_training.py  # Model training with LightGBM
├── tests/                  # Test suite
│   └── test_overall.py     # Simple tests for beginners
├── pipeline/              # Training pipeline
├── templates/             # Flask templates
├── config/               # Configuration files
├── application.py        # Flask web application
└── requirements.txt      # Python dependencies
```

## Features

- **Machine Learning Pipeline**: Complete ML pipeline with data ingestion, preprocessing, and model training
- **Web Interface**: Beautiful Flask web application for making predictions
- **Testing**: Simple test suite for beginners with clear examples
- **CI/CD**: GitHub Actions workflow with automated testing and Docker deployment
- **Cloud Ready**: AWS S3 integration and ECS deployment configuration
- **Monitoring**: MLflow integration for experiment tracking
