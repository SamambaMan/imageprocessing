run:
	docker-compose build
	docker-compose up

test:
	docker-compose -f docker-compose.test.yml build
	docker-compose -f docker-compose.test.yml run test_process make test

devconsole:
	docker-compose -f docker-compose.test.yml build
	docker-compose -f docker-compose.test.yml run test_process ipython
