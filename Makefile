init:
	python3 -m pip install -r ./app/requirements.txt
up:
	docker-compose up --build
up-prod:
	docker-compose -f docker-compose.yml -f production.yml up