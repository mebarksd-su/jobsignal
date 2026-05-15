import json
import os
from datetime import datetime


LATEST_ANALYSIS_FILE = "data/latest_analysis.json"
ANALYSIS_HISTORY_FILE = "data/analysis_history.json"


def save_latest_analysis(analysis_data):

    os.makedirs("data", exist_ok=True)

    with open(LATEST_ANALYSIS_FILE, "w") as file:
        json.dump(analysis_data, file, indent=4)


def load_latest_analysis():

    if not os.path.exists(LATEST_ANALYSIS_FILE):
        return None

    with open(LATEST_ANALYSIS_FILE, "r") as file:
        return json.load(file)


def save_analysis_to_history(analysis_data):

    os.makedirs("data", exist_ok=True)

    history = load_analysis_history()

    analysis_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": analysis_data
    }

    history.append(analysis_record)

    with open(ANALYSIS_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def load_analysis_history():

    if not os.path.exists(ANALYSIS_HISTORY_FILE):
        return []

    with open(ANALYSIS_HISTORY_FILE, "r") as file:
        return json.load(file)