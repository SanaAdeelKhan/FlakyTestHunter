from app import process_order

def test_process_order_succeeds():
    result = process_order(101)
    assert result["status"] == "success"
