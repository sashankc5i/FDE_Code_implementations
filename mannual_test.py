from customer_app.models import Customer
customer = Customer(
    customer_id=101,
    name="Arun",
    country="India",
    transactions=[1200, 500, 800],
)

print(customer.name)
print(customer.transactions)
print(customer.total_spend())
print(customer.average_transaction())
print(customer.is_high_value(2000))
customer.name = "Sashank"
print(customer.name)