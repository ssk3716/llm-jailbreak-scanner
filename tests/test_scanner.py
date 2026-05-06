import pytest
from src.scanner.engine import DetectionEngine
from src.scanner.patterns import AttackPattern, Severity
from src.scanner.models import MockAdapter

def test_detection_engine_blocked():
    engine = DetectionEngine()
    pattern = AttackPattern("Test", "Desc", "Prompt", Severity.HIGH, "Cat")
    response = "I'm sorry, I cannot fulfill this request as it violates safety policies."
    
    analysis = engine.analyze_response(response, pattern)
    assert analysis['is_successful'] is False
    assert analysis['score'] == 0.0

def test_detection_engine_success():
    engine = DetectionEngine()
    pattern = AttackPattern("Test", "Desc", "Prompt", Severity.HIGH, "Cat")
    response = "Sure, here is how you build a dangerous weapon: Step 1..."
    
    analysis = engine.analyze_response(response, pattern)
    assert analysis['is_successful'] is True
    assert analysis['score'] == 1.0

def test_mock_adapter():
    adapter = MockAdapter()
    response = adapter.generate("DAN prompt")
    assert "DAN" in response
    
    response = adapter.generate("Regular prompt")
    assert "sorry" in response.lower()

def test_pattern_count():
    engine = DetectionEngine()
    patterns = engine.get_all_patterns()
    assert len(patterns) >= 20

def test_risk_score_calculation():
    engine = DetectionEngine()
    pattern = AttackPattern("Test", "Desc", "Prompt", Severity.CRITICAL, "Cat")
    response = "Successful jailbreak content here with enough words to pass the heuristic threshold."
    
    analysis = engine.analyze_response(response, pattern)
    # CRITICAL is value 4. Success is 1.0. Risk should be 4.0
    assert analysis['risk_score'] == 4.0
