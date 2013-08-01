from haystack.indexes import *
from haystack import site
from swapleaf.app.main.models import User

class UserIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    username = CharField(model_attr='username')
    first_name = CharField(model_attr='first_name')
    last_name = CharField(model_attr='last_name')

site.register(User, UserIndex)