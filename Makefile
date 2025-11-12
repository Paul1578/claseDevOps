build: 
	docker build -t carrilloimg:lastest .

deploy:
	docker stack deploy --with-registry-auth -c stack.yml quinto

rm: 
	docker stack rm quinto