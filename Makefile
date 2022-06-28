IMAGE := metalfarmer/internal-auth-api
TAG := latest

build:
	docker build --tag $(IMAGE) .

run:
	docker run -it -p 5001:5000 $(IMAGE)

push:
	docker tag $(IMAGE):$(TAG) $(IMAGE):$(TAG)
	docker push $(IMAGE):$(TAG)