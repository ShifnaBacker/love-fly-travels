from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class Payment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_contact_india = models.CharField(max_length=15)
    customer_contact_other = models.CharField(max_length=15 ,default='')
    feedback = models.TextField(blank=True, null=True)  # Optional field
    order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.customer_name} - {self.amount} {self.currency}"
