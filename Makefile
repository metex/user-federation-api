IMAGE := metalfarmer/internal-auth-api
TAG := latest

build:
	docker build --tag $(IMAGE) .

run-local: ## If you are using the docker-compose-kong.yml for local development
	docker run --env MYSQL_HOST=localhost --env MYSQL_PORT=3308 --env MYSQL_DATABASE=users --env MYSQL_USER=root --env MYSQL_PASSWORD=secret -it -p 5001:5000 $(IMAGE)

push:
	docker tag $(IMAGE):$(TAG) $(IMAGE):$(TAG)
	docker push $(IMAGE):$(TAG)