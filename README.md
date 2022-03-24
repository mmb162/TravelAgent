# Travel Agent

## Create Virtual Environment
`python3 -m venv env`

`pip install -r requirements.txt`

## Activate Virtual Environment
`source env/bin/activate`

## Tear Down Virtual Environment
`deactivate`

## Run Application Natively

`python3 manage.py migrate`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py createsuperuser`

`python3 manage.py runserver`

http://127.0.0.1:8000/travel/

## Run Application Containerized

`docker-compose build`

`docker-compose up`

If you need to access data/

`sudo chown -R $USER:$USER .`

