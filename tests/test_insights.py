from app.services import generate_insight

def test_generate_insight():
    insight = generate_insight()
    assert isinstance(insight.metric, str)
    assert isinstance(insight.observation, str)
    assert isinstance(insight.recommendation, str)
