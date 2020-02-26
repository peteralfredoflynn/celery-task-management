build:
	docker build -t task_mgt_app .
up:
	docker-compose -f var/dev-compose.yml up --remove-orphans
down:
	docker-compose -f var/dev-compose.yml down --remove-orphans
rm:
	docker-compose -f var/dev-compose.yml rm -fsv
