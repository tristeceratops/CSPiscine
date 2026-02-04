IMAGE_NAME = stockholm

build:
	docker build -t $(IMAGE_NAME) .

run: build
	- docker run -it --rm $(IMAGE_NAME) /bin/bash

clean:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

fclean: clean
	docker rmi -f $(IMAGE_NAME)

.PHONY: build run clean fclean
