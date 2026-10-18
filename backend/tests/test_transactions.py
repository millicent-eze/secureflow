def test_list_transactions_requires_authentication(client):
    response = client.get("/transactions")

    assert response.status_code == 401


def test_create_transaction_requires_authentication(client):
    response = client.post(
        "/transactions",
        json={
            "amount": "5000.00",
            "currency": "NGN",
            "beneficiary": "Test Beneficiary",
        },
    )

    assert response.status_code == 401

def test_admin_cannot_create_customer_transaction(admin_client):
    response = admin_client.post(
        "/transactions",
        json={
            "amount": "5000.00",
            "currency": "NGN",
            "beneficiary": "Test Beneficiary",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Only customers can initiate transactions."
    )

def test_inactive_user_cannot_list_transactions(inactive_user_client):
    response = inactive_user_client.get("/transactions")

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_customer_can_only_see_own_transactions(
    client,
    customer_factory,
):
    from app.database import get_db
    from app.models.transaction import Transaction

    customer_a_id, customer_a_token = customer_factory(
        "customer-a@secureflow.test"
    )

    customer_b_id, customer_b_token = customer_factory(
        "customer-b@secureflow.test"
    )

    db_generator = client.app.dependency_overrides[get_db]()
    db = next(db_generator)

    db.add_all(
        [
            Transaction(
                user_id=customer_a_id,
                amount="5000.00",
                currency="NGN",
                beneficiary="Synthetic Beneficiary A",
                status="allow",
            ),
            Transaction(
                user_id=customer_b_id,
                amount="9000.00",
                currency="NGN",
                beneficiary="Synthetic Beneficiary B",
                status="allow",
            ),
        ]
    )

    db.commit()
    db.close()

    client.headers["Authorization"] = (
        f"Bearer {customer_a_token}"
    )

    try:
        response = client.get("/transactions")

        assert response.status_code == 200

        transactions = response.json()

        assert len(transactions) == 1
        assert transactions[0]["user_id"] == customer_a_id
        assert transactions[0]["beneficiary"] == (
            "Synthetic Beneficiary A"
        )
        assert all(
            transaction["user_id"] != customer_b_id
            for transaction in transactions
        )

    finally:
        client.headers.pop("Authorization", None)          