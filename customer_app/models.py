"""Domain models for the customer data processor."""


class Customer:
    """Represent a customer and their transaction history."""

    def __init__(
        self,
        customer_id: int,
        name: str,
        country: str,
        transactions: list[float],
    ) -> None:
        self.customer_id = customer_id
        self.name = name
        self.country = country
        self.transactions = transactions

    def total_spend(self) -> float:
        """Return the customer's total transaction value."""

        return sum(self.transactions)

    def average_transaction(self) -> float:
        """Return the customer's average transaction value."""

        if not self.transactions:
            return 0.0

        return self.total_spend() / len(self.transactions)

    def is_high_value(self, threshold: float) -> bool:
        """Return whether the customer exceeds the given spending threshold."""

        return self.total_spend() > threshold