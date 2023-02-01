
build:
	sh scripts.sh build $(version)

publish:
	sh scripts.sh publish $(version)

push-img:
	sh scripts.sh push-img $(version)

deploy:
	sh scripts.sh deploy

prestart:
	sh scripts.sh prestart

dev:
	sh scripts.sh dev

down:
	docker-compose down

rm-vols: down
	docker volume rm ubicor-api_dbdata
	docker volume ls
