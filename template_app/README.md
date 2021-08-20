# Flask app template
## 1. Use
- Python version: 3.7
- Setting enviroment:
```console
python -m venv env
```
- Run enviroment:
```console
env\Scripts\activate
```
- Install library:
```console
	pip install -r requirements.txt
```
- To connect database: update file ".env":
	DATABASE_URI=mysql://{user}:{password}@{host}/{database_name}
	As default, this was set as:
		DATABASE_URI=mysql://root:12345@localhost/demo
- Run:
```console
cd template_app
python manage.py run
```
- Test:
```console
python manage.py test
```
## 2. Example
- Go to Swagger UI: http://127.0.0.1:5000
- Get all projects storaged in database: http://127.0.0.1:5000/projects
