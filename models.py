from playhouse.postgres_ext import *
import db


class BaseModel(Model):
    class Meta:
        database = db.pg_db
        order_by = 'id'


class TypeofCategory(BaseModel):
    id = AutoField()
    name = CharField(max_length=63, unique=True, null=False)
    weekly_limit = IntegerField(null=True)
    monthly_limit = IntegerField(null=True)


class Category(BaseModel):
    id = AutoField()
    name = CharField(max_length=63, unique=True, null=False)
    accepted_payments_type = CharField(max_length=4, null=False)
    is_additional_info_needed = BooleanField(null=False)
    fixed_price = IntegerField(null=True)
    aliases = TextField(null=True)
    type_id = ForeignKeyField(TypeofCategory, on_delete='CASCADE')


class Expense(BaseModel):
    id = AutoField()
    amount = DecimalField(max_digits=12, decimal_places=2, null=False)
    time_creating = DateTimeTZField(null=False)
    category_id = ForeignKeyField(Category, on_delete='SET NULL')
    payment_type = CharField(max_length=4, null=False)
    additional_info = CharField(max_length=255, null=True)
    raw_text = TextField(null=True)
