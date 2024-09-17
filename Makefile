up : 
	docker compose up -d --remove-orphans
build : 
	docker compose build --remove-orphans
up-build : 
	docker compose up -d --build
down :
	docker compose down