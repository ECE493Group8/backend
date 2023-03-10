flask = flask --app backend

run:
	$(flask) run

docs:
	$(flask) openapi write --format=yaml openapi.yaml