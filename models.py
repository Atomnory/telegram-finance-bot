from playhouse.postgres_ext import *
import db


class BaseModel(Model):
    class Meta:
        database = db.pg_db
        order_by = 'id'


class TypeofCategory(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=63)


class Budget(BaseModel):
    type_id = ForeignKeyField(TypeofCategory, primary_key=True, on_delete='CASCADE')
    weekly_limit = IntegerField()
    monthly_limit = IntegerField()

    class Meta:
        order_by = 'type_of_category_id'


class Category(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=63)
    is_cash_accepted = BooleanField()
    is_card_accepted = BooleanField()
    is_additional_info_needed = BooleanField()
    aliases = TextField()
    type_id = ForeignKeyField(TypeofCategory, on_delete='CASCADE')


class FixedPrice(BaseModel):
    category_id = ForeignKeyField(Category, primary_key=True, on_delete='CASCADE')
    price = IntegerField()

    class Meta:
        order_by = 'category_id'


class Expense(BaseModel):
    id = AutoField(primary_key=True)
    amount = DecimalField(max_digits=12, decimal_places=2)
    time_creating = DateTimeTZField()
    category_id = ForeignKeyField(Category, on_delete='CASCADE')
    payment_type = CharField(max_length=4)
    additional_info = CharField(max_length=255, null=True)
    raw_text = TextField(null=True)
