"""Domain models for customer data."""

from dataclasses import dataclass


@dataclass
class Transaction:
    """Represent a customer transaction."""

    transaction_id: str
    amount: float
    currency: str


@dataclass
class Customer:
    """Represent a customer."""

    customer_id: int
    name: str
    country: str
    transactions: list[Transaction]

    def total_spend(self) -> float:
        """Calculate total customer spending."""

        return sum(
            transaction.amount
            for transaction in self.transactions
        )

    def average_transaction(self) -> float:
        """Calculate average transaction value."""

        if not self.transactions:
            return 0.0

        return self.total_spend() / len(self.transactions)

    def is_high_value(
        self,
        threshold: float,
    ) -> bool:
        """Determine whether customer is high value."""

        return self.total_spend() > threshold