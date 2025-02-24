mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser


udb:
	rm -rf db.sqlite3
	rm -rf ticket/migrations/*
	rm -rf authentication/migrations/*
	touch ticket/migrations/__init__.py
	touch authentication/migrations/__init__.py
	python3 manage.py makemigrations
	python3 manage.py migrate

celery:
	celery -A root worker --loglevel=info

sort:
	black .
	isort .


#from scripts.fake_products import create_fake_products, create_fake_categories
#create_fake_categories(num_categories=10)
#create_fake_products(num_products=50)

