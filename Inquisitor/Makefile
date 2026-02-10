CONT_1 := container1
CONT_2 := container2

all: build

build:
	docker compose up -d

stop:
	docker compose stop

start:
	docker compose start

restart: stop start

clean: stop

fclean: clean
	docker compose down --remove-orphans --volumes --rmi all || true
	docker system prune -a --volumes -f || true

check:
	@docker ps -a
	@echo ""
	@docker volume ls
	@echo ""
	@docker images -a
	@echo ""
	@docker network ls

re: fclean build

.PHONY: all build stop start restart clean fclean check re