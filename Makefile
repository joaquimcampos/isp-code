help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-21s\033[0m %s\n", $$1, $$2}'

run-code: python3 face_video.py $(ARGS)

# Codestyle scripts

lint: ## Ensures the code is properlly formatted
	pycodestyle face_video.py
	isort --settings-path=./setup.cfg --check-only face_video.py

format:  ## format the code accordig to the configuration
	autopep8 -ir face_video.py
	isort --settings-path=./setup.cfg face_video.py


# Pipenv scripts - dependency management

lock: ## Refresh pipfile.lock
	pipenv lock

requirements: ## Refresh requirements.txt from pipfile.lock
	pipenv requirements > requirements.txt

requirements_dev: ## Refresh requirements-dev.txt from pipfile.lock
	pipenv requirements --dev > requirements-dev.txt

check: ## Scan dependencies for security vulnerabilities
	pipenv check

update: ## Update dependencies in pipfile and refresh pipfile.lock
	pipenv update

update_dev: ## Update all dependencies in pipfile and refresh pipfile.lock
	pipenv update --dev
