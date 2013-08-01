web: python manage.py runserver 0.0.0.0:$PORT --noreload
loaddata: python load_school_data.py && python load_book_data1.py
loadschool: python load_school_data.py 
loadbook: python load_book_data1.py
setupdb: python manage.py schemamigration main --initial && python manage.py schemamigration tastypie --initial && python manage.py syncdb && python manage.py migrate main && python manage.py migrate tastypie && python manage.py migrate --fake
