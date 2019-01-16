## Construye el contenedor localmente
build:
	docker build --rm -t checks_balances:latest .
## Corre el contenedor hecho en build
run:
	docker run -d -p 5000:5000  checks_balances:latest
## Hace push el contenedor creado hacia el repositorio que esté configurado
push:
	@read -p "Enter repo name:" name; \
	docker push  $$name/checks_balances:latest
## Corre los tests creados
test:
	python -m venv test-venv
	\
	source test-venv/bin/activate; \
	pip install --upgrade pip
	pip install -r requirements.txt
	pytest
	deactivate
	rm -R test-venv
