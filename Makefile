up : 
	docker compose up -d
build : 
	docker compose build
up-build : build up 
down :
	docker compose down