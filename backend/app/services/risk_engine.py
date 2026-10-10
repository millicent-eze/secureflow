from decimal import Decimal


def assess_transaction_risk(
    amount: Decimal,
    average_transaction: Decimal,
    is_new_device: bool = False,
    is_new_beneficiary: bool = False,
    unusual_location: bool = False,
    failed_login_attempts: int = 0,
    unusual_time: bool = False,
) -> dict:
    score = 0
    reasons = []

    # Rule 1: Detect unusually large transactions.
    if average_transaction > 0:
        ratio = amount / average_transaction

        if ratio >= 10:
            score += 30
            reasons.append(
                "Transaction amount is at least 10 times the user's average."
            )
        elif ratio >= 5:
            score += 20
            reasons.append(
                "Transaction amount is at least 5 times the user's average."
            )

    # Rule 2: Detect a new device.
    if is_new_device:
        score += 20
        reasons.append("Transaction originated from a new device.")

    # Rule 3: Detect a new beneficiary.
    if is_new_beneficiary:
        score += 20
        reasons.append("Transaction is being sent to a new beneficiary.")

    # Rule 4: Detect unusual locations.
    if unusual_location:
        score += 15
        reasons.append("Transaction originated from an unusual location.")

    # Rule 5: Detect repeated failed login attempts.
    if failed_login_attempts >= 3:
        score += 15
        reasons.append("Multiple failed login attempts were detected.")

    # Rule 6: Detect unusual transaction times.
    if unusual_time:
        score += 10
        reasons.append("Transaction occurred at an unusual time.")

    # Prevent scores from exceeding 100.
    score = min(score, 100)

    # Determine the risk decision.
    if score >= 60:
        decision = "BLOCK"
        risk_level = "HIGH"
    elif score >= 30:
        decision = "REVIEW"
        risk_level = "MEDIUM"
    else:
        decision = "ALLOW"
        risk_level = "LOW"

    # Return an explainable risk assessment.
    return {
        "risk_score": score,
        "decision": decision,
        "risk_level": risk_level,
        "reasons": reasons,
    }