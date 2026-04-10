# Data-Extraction-from-Livestreams


This repository contains the codes of my project work of the IoT & Big Data course of the Postgraduate Applied Artificial Intelligence program at Erasmushogeschool Brussels.

For the example project of the course github please visit : https://github.com/mdequanter/PostGraduatAI

---

# Installation

Follow the steps below to set up the project locally.

## 1. Clone the repository

git clone https://github.com/yourusername/Data-Extraction-from-Livestreams.git
cd Data-Extraction-from-Livestreams

## 2. Create a Python virtual environment

python -m venv venv

## 3. Activate the virtual environment (Linux)

source venv/bin/activate

## 4. Install the required packages

pip install -r requirements.txt

## 5. Run the application

python livestream_crowd_control.py

# Brief project content

This script will open the livestream given in the config python file: uncomment an import statement of a config.py file in the IMPORT PARAMETERS section of livestream_crowd_control.py file. It detects objects (given in the config file such as person, dog, etc) in predefined windows given by the zooms values of the STREAMS dictionary in the config file. It creates a SQL or CSV file with the count maximums in every second for each window and each object. If the STREAMS dictionary contains more livestreams, each livestream will have a separate data file. This data can be then further processed for example in crowd control IoT/Big Data applicaitons.


# Purpose

This repository is intended as a **showcase of my project work** and comes without any warranties or liabilities: use it for your own fun on your own risk to experiment with:

- livestream(s) processing
- computer vision
- objects detection and counting
- IoT data pipelines
- Big Data extraction from livestream(s)
- AI-based video analysis
