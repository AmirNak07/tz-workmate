import pytest


@pytest.fixture
def test_data():
    return [
        {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
        {
            "name": "galaxy s23 ultra",
            "brand": "samsung",
            "price": "1199",
            "rating": "4.8",
        },
        {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
        {"name": "iphone 14", "brand": "apple", "price": "799", "rating": "4.7"},
        {"name": "galaxy a54", "brand": "samsung", "price": "349", "rating": "4.2"},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
        {"name": "iphone se", "brand": "apple", "price": "429", "rating": "4.1"},
        {"name": "galaxy z flip", "brand": "samsung", "price": "999", "rating": "4.6"},
        {"name": "redmi 10c", "brand": "xiaomi", "price": "149", "rating": "4.1"},
        {"name": "iphone 13 mini", "brand": "apple", "price": "599", "rating": "4.5"},
    ]
