from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    """
    BaseModel class including base fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return '{} {} - {}'.format(
            self.first_name, self.last_name, self.username)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Account(BaseModel):
    number = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True)
    balance = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} {}'.format(
            self.number, self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Transaction(BaseModel):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        unique=True)
    type = models.CharField(max_length=10, blank=True)
    amount = models.FloatField()
    description = models.CharField(max_length=254, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {} - {} - {}'.format(
            self.id, self.account.number, self.type, self.amount)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class Loan(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    interest_rate = models.FloatField()
    status = models.CharField(max_length=20)
    deadline = models.DateField()

    def __str__(self):
        return '{} {}: {} - {}'.format(
            self.user.first_name,
            self.user.last_name,
            self.amount,
            self.created_at)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


class LoanProfile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return '{} {}: {}'.format(
            self.user.first_name, self.user.last_name, self.score)

    class Meta:
        verbose_name = 'Loan Profile'
        verbose_name_plural = 'Loan Profiles'


class LoanPayment(BaseModel):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=20, blank=True)
    payment_date = models.DateTimeField(null=True)
    deadline = models.DateField(null=True)

    def __str__(self):
        return '{}: {} - {}'.format(
            self.loan.id, self.amount, self.created_at)

    class Meta:
        verbose_name = 'Loan Payment'
        verbose_name_plural = 'Loan Payments'
