from dataclasses import dataclass
import uuid

@dataclass
class Transaction:
    id: str
    type: str  # "income" or "expense"
    title: str
    description: str
    amount: float
    category: str
    date: str  # "YYYY-MM-DD"
    payment_method: str

    @classmethod
    def create(cls, type: str, title: str, description: str, amount: float, category: str, date: str, payment_method: str) -> "Transaction":
        return cls(
            id=str(uuid.uuid4()),
            type=type,
            title=title,
            description=description,
            amount=amount,
            category=category,
            date=date,
            payment_method=payment_method
        )
