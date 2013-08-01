from django.utils import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from swapleaf.app.main.models import Institution

# Implement later for full autocomplete support
@dajaxice_register
def autocomplete(request):
	return simplejson.dumps({})
	