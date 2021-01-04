.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-media clean-output

clean-output:
	rm -f output/*

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-media:
	rm -rf rec_demo/media
	mkdir rec_demo/media


patch: clean ## package and upload a release
	python ./scripts/bump.py --action=patch


minor: clean ## package and upload a release
	python ./scripts/bump.py --action=minor

backup-prod:
	python ./scripts/backup.py --env=prod

backup-staging:
	python ./scripts/backup.py --env=staging

backup: backup-staging

stop-containers:
	docker stop $$(docker ps -qa)

test: stop-containers
	docker-compose -f local.yml run --service-ports django python manage.py test --settings=config.settings.test --exclude-tag=TO-FIX --exclude=PROD
	#./scripts/test_cypress.sh

test-finance: stop-containers
	docker-compose -f local.yml run --service-ports django python manage.py test alpha_clinic.finance.tests --settings=config.settings.test --exclude-tag=TO-FIX --exclude=PROD
	#./scripts/test_cypress.sh

check:
	docker-compose -f local.yml run --service-ports django python manage.py check --deploy

release-patch: check clean-media test patch #build-spa
	tput bel

release-minor: check clean-media test minor #build-spa
	tput bel

heroku: backup
	git push origin master
	git push origin develop
	git push --tags
	git push heroku master
	heroku run python manage.py migrate
