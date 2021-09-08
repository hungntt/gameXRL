# gameXRL
Repo for white paper XRL
##Database Architecture:
![erd.png](erd.png)

## Architecture
    .
    ├── ...
    ├── app              
    │   ├── routes         
    │   │   ├── forms.py                # Create form to fill from front-end form
    │   │   ├── routes.py               # Run main from here (contains controller)
    │   ├── templates            
    │   │   ├── _formhelpers.html       # Render forms
    │   └────── index.html              # Index page
    ├── db                              # Database
    │   ├── api.py                      # API query to insert/read data from database
    │   ├── connect_db.py               # Connect to database through a SSHTunnelForwarder
    │   ├── create_db.py                # Create models on database      
    ├── ref_app                         # Some references 
    ├── requirements.txt                # Some requirements 
    └── README.md

## Flask app template
### 1. Use
- Python version: 3.7
- Setting environment:
```console
python -m venv env
```
- Run environment:
```console
env\Scripts\activate
```
- Install library:
```
pip install -r requirements.txt
```
- To connect database: update file ".env":
```
 DATABASE_URI=mysql://{user}:{password}@{host}/{database_name}
```
- As default, this was set as:
```
DATABASE_URI=mysql://root:12345@localhost/demo
```
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
