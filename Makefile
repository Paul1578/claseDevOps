build: 
	docker build -t carrilloimg:latest .

deploy:
	docker stack deploy --with-registry-auth -c stack.yml quinto

rm: 
	docker stack rm quinto