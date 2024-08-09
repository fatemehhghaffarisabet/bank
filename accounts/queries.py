import time
import random, string
from django.db.models.functions import Cast
from django.db.models import Max, Sum, F, BigIntegerField, Q
from .models import Person, Account

def generate():
    persons = []
    accounts = []
    for i in range(1000000):
        length = random.randint(1, 10)
        persons.append(Person(
            first_name=''.join(random.choices(string.ascii_lowercase, k=length)),
            last_name=''.join(random.choices(string.ascii_lowercase, k=length)),
            ssn=''.join(random.choices(string.digits, k = 10)),
        ))
    persons = Person.objects.bulk_create(persons)
    for i in range(20000):
        accounts.append(Account(
            balance = random.randint(0, 1000000),
            owner = random.choice(persons),
        ))
    accounts = Account.objects.bulk_create(accounts)


def account_list():
    return Account.objects.values('balance', 'owner__first_name')


def max_value():
    return Account.objects.aggregate(Max('balance'))

def min_values():
    return Account.objects.values('balance').order_by('balance')[:5:-1]

def transfer(origin_id, destinationـid, mony):
    first = Account.objects.get(id=origin_id)
    secend = Account.objects.get(id=destinationـid)
    if first.balance < mony:
        return 'the balance is lower than required mony.'
    else:
        first.balance = first.balance - mony
        secend.balance = secend.balance + mony
        first.save()
        secend.save()

def id_more_than_balance():
    id = F('id')
    return Account.objects.filter(balance__lt=id)

def ssn_more_than_balamce():
    return Account.objects.annotate(ssn=Cast('owner__ssn', output_field=BigIntegerField())).filter(ssn__gte=F('balance'))

def search():
    start = time.time()
    result = Account.objects.filter(Q(balance__lt=1000000) | Q(balance__gt=2000000))
    print(time.time() - start)
    return result

def sum_balance():
    return Person.objects.annotate(total_balance=Sum("account__balance"))