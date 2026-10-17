from decimal import Decimal


# Demo thresholds for SecureFlow.
# These are configurable starting points, not real banking rules.
REVIEW_AMOUNT_THRESHOLD = Decimal("150000")
BLOCK_AMOUNT_THRESHOLD = Decimal("500000")


def assess_transaction_risk(
    amount: Decimal,
    average_transaction: Decimal | None = None,
    is_new_device: bool = False,
    is_new_beneficiary: bool = False,
    unusual_location: bool = False,
    failed_login_attempts: int = 0,
    unusual_time: bool = False,
) -> dict:
    score = 0
    reasons = []

    # Rule 1: Check the transaction amount against demo thresholds.
    if amount >= BLOCK_AMOUNT_THRESHOLD:
        score += 60
        reasons.append(
            "Transaction amount meets the high-risk blocking threshold."
        )
    elif amount >= REVIEW_AMOUNT_THRESHOLD:
        score += 30
        reasons.append(
            "Transaction amount meets the manual review threshold."
        )

    # Rule 2: Compare the amount with the user's previous transaction average.
    # Skip this rule when the user has no transaction history.
    if average_transaction is not None and average_transaction > 0:
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

    # Rule 3: Add points for other suspicious signals.
    if is_new_device:
        score += 20
        reasons.append("Transaction originated from a new device.")

    if is_new_beneficiary:
        score += 20
        reasons.append("Transaction is being sent to a new beneficiary.")

    if unusual_location:
        score += 15
        reasons.append("Transaction originated from an unusual location.")

    if failed_login_attempts >= 3:
        score += 15
        reasons.append("Multiple failed login attempts were detected.")

    if unusual_time:
        score += 10
        reasons.append("Transaction occurred at an unusual time.")

    # Cap the score at 100.
    score = min(score, 100)

    # Make the final decision.
    # A transaction meeting the blocking amount threshold is always blocked.
    if amount >= BLOCK_AMOUNT_THRESHOLD or score >= 60:
        decision = "BLOCK"
        risk_level = "HIGH"
    elif score >= 30:
        decision = "REVIEW"
        risk_level = "MEDIUM"
    else:
        decision = "ALLOW"
        risk_level = "LOW"

    return {
        "risk_score": score,
        "decision": decision,
        "risk_level": risk_level,
        "reasons": reasons,
    }
