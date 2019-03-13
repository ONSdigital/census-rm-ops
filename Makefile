build:
	pipenv install --dev

lint:
	pipenv run flake8 ./app ./tests
	pipenv check ./app ./tests

test: lint
	pipenv run pytest --cov-report term-missing --cov app --capture no

start:
	pipenv run python run.py

docker: test
	docker build -t eu.gcr.io/census-rm-ci/census-rm-ops .

docker-run: docker
	docker run --network=censusrmdockerdev_default  -p 8003:80 eu.gcr.io/census-rm-ci/census-rm-ops:latest
