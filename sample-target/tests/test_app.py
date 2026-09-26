from unittest.mock import patch
from app import process_order

def test_process_order_succeeds():
    # Pin random.uniform to 0.0 so delay never exceeds the 0.2 timeout threshold
    with patch("app.random.uniform", return_value=0.0):
        result = process_order(101)
    assert result["status"] == "success"
