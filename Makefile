Make run:
	docker-compose up --build

Make migrate:
	python manage.py migrate

Make migrations:
	python manage.py makemigrations

Make runserver:
	python manage.py runserver