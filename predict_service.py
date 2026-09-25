"""
Predict Service — wraps ml/predict.py module.
"""

import sys
import os

# Add ml/ directory to path so we can import ml/predict.py
ML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml")
ML_DIR = os.path.normpath(ML_DIR)
if ML_DIR not in sys.path:
    sys.path.insert(0, ML_DIR)

from predict import predict_cost   # resolves to ml/predict.py


def predict_trip_cost(
    destination: str,
    days: int,
    travelers: int,
    transport_type: str,
    hotel_type: str,
) -> dict:
    """Wrapper around ml/predict.py predict_cost. Returns structured prediction."""
    return predict_cost(
        destination=destination,
        days=days,
        travelers=travelers,
        transport_type=transport_type,
        hotel_type=hotel_type,
    )
