flask = flask --app backend
gunicorn = gunicorn 'backend:app'

# Run a dev server
dev:
	$(flask) run --host 0.0.0.0 --port 5000

# Start service
start:
	sudo systemctl start word2med-backend

# Stop service
stop:
	sudo systemctl stop word2med-backend

# Get status of the service
status:
	sudo systemctl status word2med-backend

# Restart the service to apply any changes
restart:
	sudo systemctl restart word2med-backend

# Generate documentation yaml, hosted on github pages
docs:
	$(flask) openapi write --format=yaml openapi.yaml

# Run unit tests - TODO: use for all tests once model is set up
test:
	pytest test_endpoints.py test_schemas.py test_word2med.py