import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Import models so SQLAlchemy registers their tables.
from app.models.user import User
from app.models.transaction import Transaction
from app.models.risk_assessment import RiskAssessment


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def admin_client(client):
    from app.models.user import User
    from app.security.token import create_access_token
    from app.database import get_db

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)

    admin = User(
        email="admin@secureflow.test",
        full_name="Test Admin",
        password_hash=None,
        role="admin",
        is_active=True,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = create_access_token(
        subject=str(admin.id),
        role=admin.role,
    )

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    try:
        yield client
    finally:
        client.headers.pop("Authorization", None)
        db.close()

@pytest.fixture
def inactive_user_client(client):
    from app.models.user import User
    from app.security.token import create_access_token
    from app.database import get_db

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)

    inactive_user = User(
        email="inactive@secureflow.test",
        full_name="Inactive Test User",
        password_hash=None,
        role="customer",
        is_active=False,
    )

    db.add(inactive_user)
    db.commit()
    db.refresh(inactive_user)

    token = create_access_token(
        subject=str(inactive_user.id),
        role=inactive_user.role,
    )

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    try:
        yield client
    finally:
        client.headers.pop("Authorization", None)
        db.close()

@pytest.fixture
def customer_factory(client):
    from app.models.user import User
    from app.security.token import create_access_token
    from app.database import get_db

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)

    created_users = []

    def create_customer(email):
        customer = User(
            email=email,
            full_name="Test Customer",
            password_hash=None,
            role="customer",
            is_active=True,
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        token = create_access_token(
            subject=str(customer.id),
            role=customer.role,
        )

        created_users.append((customer.id, token))

        return customer.id, token

    try:
        yield create_customer
    finally:
        db.close()               
