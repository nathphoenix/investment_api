from ma import ma
from models.investment import InvestmentModel




class InvestmentDeleteSchema(ma.ModelSchema):
    # this is weird in python, defining a class inside a class but you can do it with marshmallow
    # You can say a field is for loading the data and not for dumping it
    class Meta:
        model = InvestmentModel    # this is extending the functionality of marshmallow schema and link up the user model
        load_only = ("id")  # meaning the creator field is only for loading the data, it should not be returned
                                   # when dumping  the data
        dump_only = ("id",)
        include_fk = True


class InvestmentSchema(ma.ModelSchema):
    # this is weird in python, defining a class inside a class but you can do it with marshmallow
    # You can say a field is for loading the data and not for dumping it
    class Meta:
        model = InvestmentModel    # this is extending the functionality of marshmallow schema and link up the user model
        load_only = ("creator", "id")  # meaning the creator field is only for loading the data, it should not be returned
                                   # when dumping  the data
        dump_only = ("id",)
        include_fk = True
        # must be included since we are returning the store_id as it is a foreign key