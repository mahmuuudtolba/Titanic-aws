# Salary Prediction With GCP
 
This is a implementation of the classification model for salary prediction.

## Requirements
- python 3.10 or later


#### install python using Anaconda

## Installation 

```bash
conda create --prefix ./venv python=3.11 -y
```

### Install the required packages
```bash
$ pip install -r requirements.txt
```

### Run application locally
Run the pipeline
```bash
$ python pipeline/training_pipeline.py
```

Lanuch the flask app
```bash
$ python application.py
```

## Docker
### Build the image
```bash
docker build -t titanic-image .
```
### Run the container

```bash
docker run --name titanic-container -p 5000:5000 -v ./.aws:/root/.aws:ro titanic-image
```
