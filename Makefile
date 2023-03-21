flask = flask --app backend
gunicorn = gunicorn 'backend:app'

run:
	$(flask) run

# Run with 2 workers
prod:
	$(gunicorn) -w 2 -b 0.0.0.0

docs:
	$(flask) openapi write --format=yaml openapi.yaml