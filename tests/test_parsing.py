from medsearch.parsing import extract_slots

def test_basic_slots():
    q = "lung ct pneumonia classification adult"
    slots = extract_slots(q)
    assert "CT" in slots["modality"]
    assert "lung" in slots["organs"]
    assert "pneumonia" in slots["diseases"]
    assert "classification" in slots["tasks"]