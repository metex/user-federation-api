## User federation Api
### Usage
```bash
make run ## To run the webserver
make build ## To build a docker image
make push ## To push a docker image to docker hub
```

### Http commands
```bash
curl -v --header "Content-Type: application/json" --request POST
  --data '{"email":"john1@gmail.com","password":"1234567"}' http://localhost:5000/validate

curl -v --header "Content-Type: application/json" --request GET http://localhost:5000/user_info?id=1
```