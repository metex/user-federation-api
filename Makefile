IMAGE := metalfarmer/internal-auth-api
TAG := latest

build:
	docker build --tag $(IMAGE) .

run:
	docker run --env MYSQL_HOST=192.168.1.75 --env MYSQL_PORT=3307 --env MYSQL_DATABASE=StageAccount --env MYSQL_USER=root --env MYSQL_PASSWORD=secret -it -p 5001:5000 $(IMAGE)

push:
	docker tag $(IMAGE):$(TAG) $(IMAGE):$(TAG)
	docker push $(IMAGE):$(TAG)