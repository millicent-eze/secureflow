from decimal import Decimal

from app.services.risk_engine import assess_transaction_risk


def test_low_amount_is_allowed():
    result = assess_transaction_risk(
        amount=Decimal("5000")
    )

    assert result["decision"] == "ALLOW"
    assert result["risk_level"] == "LOW"
    assert result["risk_score"] == 0


def test_review_amount_requires_review():
    result = assess_transaction_risk(
        amount=Decimal("150000")
    )

    assert result["decision"] == "REVIEW"
    assert result["risk_level"] == "MEDIUM"
    assert result["risk_score"] == 30


def test_high_amount_is_blocked():
    result = assess_transaction_risk(
        amount=Decimal("600000")
    )

    assert result["decision"] == "BLOCK"
    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] == 60


def test_new_device_increases_risk_score():
    result = assess_transaction_risk(
        amount=Decimal("5000"),
        is_new_device=True,
    )

    assert result["risk_score"] == 20
    assert result["decision"] == "ALLOW"
    assert result["risk_level"] == "LOW"
    assert "Transaction originated from a new device." in result["reasons"]   



def test_new_beneficiary_increases_risk_score():
    result = assess_transaction_risk(
        amount=Decimal("5000"),
        is_new_beneficiary=True,
    )

    assert result["risk_score"] == 20
    assert result["decision"] == "ALLOW"
    assert result["risk_level"] == "LOW"
    assert (
        "Transaction is being sent to a new beneficiary."
        in result["reasons"]
    )


def test_three_failed_login_attempts_increase_risk_score():
    result = assess_transaction_risk(
        amount=Decimal("5000"),
        failed_login_attempts=3,
    )

    assert result["risk_score"] == 15
    assert result["decision"] == "ALLOW"
    assert result["risk_level"] == "LOW"
    assert (
        "Multiple failed login attempts were detected."
        in result["reasons"]
    )


    