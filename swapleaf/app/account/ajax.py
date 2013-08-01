from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from swapleaf.app.main.models import Institution

@dajaxice_register
def get_data_by_state(request,state_value):
	try:
		query = Institution.objects.filter(state=state_value).order_by("name")
		result = []
		for i in range(0,len(query)):
			obj = query[i]
			result.append([obj.city,obj.name,obj.id])
		return simplejson.dumps(result)
	except:
		return simplejson.dumps({})
	

@dajaxice_register
def get_institution_by_city(request,state_value,city_value):
	try:
		query = None
		if city_value == "None":
			query = Institution.objects.filter(state=state_value).order_by("name")
		else:
			query = Institution.objects.filter(city=city_value).order_by("name")
		result = []
		for i in range(0,len(query)):
			obj = query[i]
			result.append([obj.name,obj.id])
		return simplejson.dumps(result)
	except:
		return simplejson.dumps({})