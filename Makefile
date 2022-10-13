bold := $(shell tput bold)
sgr0 := $(shell tput sgr0)
red := $(shell tput setaf 1)
green := $(shell tput setaf 2)

.ONESHELL:

prep_venv:
	pip install -U pip wheel setuptools pip-tools

install_packages: ## Install python requirements
	pip-sync requirements/requirements.txt

install_dev_packages: ## Install python requirements
	pip-sync requirements/dev-requirements.txt

project: prep_venv install_packages build

dev: prep_venv install_dev_packages build

build: clean loaddata

truncatedb: ## truncate database tables
	python manage.py truncatedb

resetdb: ## truncate database tables
	python manage.py reset_db # from django_extensions
	@printf '\nRecreating database - $(bold)$(green)DONE!$(sgr0)\n\n'
	python manage.py migrate
	@printf '\nDjango migrations - $(bold)$(green)DONE!$(sgr0)\n\n'

reset: resetdb clean loaddata

clean: ## Clean sandbox images,cache,static and database
	# Remove media
	-rm -rf media/images media/author_photos media/original_images media/user_avatars

loadusers: ## Load user data into sandbox
	cp -r sample/user_avatars/* media/user_avatars
	python manage.py loaddata sample/users.json

copyassets:
	cp -r sample/user_avatars/* media/user_avatars
	cp -r sample/author_photos/* media/author_photos

loaddata: ## Import fixtures
	mkdir -p media/images media/original_images media/author_photos media/user_avatars
	cp -r sample/original_images/* media/original_images
	cp -r sample/images/* media/images
	cp -r sample/user_avatars/* media/user_avatars
	cp -r sample/author_photos/* media/author_photos
	@printf '\nCopied image assets - $(bold)$(green)DONE!$(sgr0)\n\n'

	# Delete existing content_types and auth.Permission
	python manage.py delete_existing_content

	# Import some fixtures, order is important as JSON fixtures include primary keys
	python manage.py loaddata sample/sites.json sample/django_auth.json \
	sample/users.json sample/content_types.json sample/taggit.json \
	sample/cms.json sample/wagtailcore.json sample/wagtailimages.json

	python manage.py update_published_at
	@printf '\nLoaded fixtures  - $(bold)$(green)DONE!$(sgr0)\n\n'

runseeds:
	mkdir -p media/images media/author_photos media/original_images media/user_avatars
	cp -r sample/original_images/* media/original_images
	cp -r sample/images/* media/images
	cp -r sample/user_avatars/* media/user_avatars
	cp -r sample/author_photos/* media/author_photos
	@printf '\nCopied image assets - $(bold)$(green)DONE!$(sgr0)\n\n'
	python manage.py loaddata sample/sites.json  sample/authors.json
	python manage.py load_article_data
	@printf '\nRunning Seeds  - $(bold)$(green)DONE!$(sgr0)\n\n'

dumpdata: # Export data
	python manage.py dumpdata sites > sample/sites.json
	python manage.py dumpdata auth > sample/django_auth.json
	python manage.py dumpdata neuaccounts > sample/users.json
	python manage.py dumpdata contenttypes > sample/content_types.json
	python manage.py dumpdata wagtailcore > sample/wagtailcore.json
	python manage.py dumpdata wagtailimages > sample/wagtailimages.json
	python manage.py dumpdata taggit > sample/taggit.json
	python manage.py dumpdata neucms > sample/cms.json

lint: ## Run flake8 and isort checks
	flake8 outlet/
	isort -c -q --diff outlet/

#######################
# Translations Handling
#######################
extract_translations: ## Extract strings and create source .po files
	django-admin.py makemessages -a

compile_translations: ## Compile translation files and create .mo files
	django-admin.py compilemessages

######################
# Project Management
######################
clean_project: ## Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt
