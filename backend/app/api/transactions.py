from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.risk_assessment import RiskAssessment
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.security.dependencies import get_current_user
from app.services.risk_engine import assess_transaction_risk


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can initiate transactions.",
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive.",
        )

    average_transaction = db.scalar(
        select(func.avg(Transaction.amount)).where(
            Transaction.user_id == current_user.id
        )
    )

    if average_transaction is not None:
        average_transaction = Decimal(str(average_transaction))

    risk_result = assess_transaction_risk(
        amount=transaction_data.amount,
        average_transaction=average_transaction,
    )

    transaction = Transaction(
        user_id=current_user.id,
        amount=transaction_data.amount,
        currency=transaction_data.currency.upper(),
        beneficiary=transaction_data.beneficiary,
        status=risk_result["decision"].lower(),
    )

    try:
        db.add(transaction)
        db.flush()

        risk_assessment = RiskAssessment(
            transaction_id=transaction.id,
            risk_score=risk_result["risk_score"],
            decision=risk_result["decision"],
            risk_level=risk_result["risk_level"],
            reasons="; ".join(risk_result["reasons"]),
        )

        db.add(risk_assessment)
        db.commit()
        db.refresh(transaction)

    except Exception:
        db.rollback()
        raise

    return transaction


@router.get(
    "",
    response_model=list[TransactionResponse],
)
def list_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "customer":
        statement = select(Transaction).where(
            Transaction.user_id == current_user.id
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Use an authorized staff investigation workflow.",
        )

    return db.scalars(
        statement.order_by(Transaction.id.desc())
    ).all()
