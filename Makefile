
build:
	sh scripts.sh build $(version)

publish:
	sh scripts.sh publish $(version)

prestart:
	sh scripts.sh prestart

dev:
	sh scripts.sh dev

down:
	docker compose down

rm-vols: down
	docker volume rm ubicor-api_dbdata
	docker volume ls