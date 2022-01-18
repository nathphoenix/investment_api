from ma import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.ModelSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user",) #we don't want to dump the user information as well as user id when we dump
        dump_only = ("id", "expired_at", "confirmed") # this is what we are not going to pass to ths model 
        include_fk = True  # so that the foreign key and user_id isn't included in the dump


class ConfirmationListSchema(ma.ModelSchema):
    # this is weird in python, defining a class inside a class but you can do it with marshmallow
    # You can say a field is for loading the data and not for dumping it
    class Meta:
        model = ConfirmationModel   # this is extending the functionality of marshmallow schema and link up the user model
        load_only = ()   # meaning the password field is only for loading the data, it should not be returned
        # what  is hidden from users                 # when dumping  the data
        dump_only = ("id",  "expired_at", "confirmed",)
        include_fk = True
        