# gameXRL
Repo for white paper XRL
## Web Interface
### Pre-install dependencies
- Install requirements
```
pip install -r requirements
```
### Setup Database
- Create Database
  - Change ```mode='local'``` if you want to run on the local database
```
python db/create_db.py
```
- Customize the database schema in ```db/create_db.py```
- Change the name of db to not interfere with other database: ```DB_NAME = 'xxx'```
- Look for function ```save_obs_to_db()``` in ```agent/test.py``` to see how to insert an observation into the database.
- Create more API functions in ```db/api.py```.
- Remember to call ```API.close_connection()``` after finishing queries to database.
- Run web server
```
python app/routes/routes.py
```
### Access to Web server
- Set up SSH if not have SSH key pair yet: https://pastebin.pl/view/62678967.
- After setting up SSH, input local public key to the IRender server (Password: Khang112@).
```
cat ~/.ssh/id_rsa.pub | ssh -p 2056 -t administrator@58.186.80.21 "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
```
- From now, connect directly to the IRender server without inputting the password.
- Access to the web server, run this command in the terminal:
```
ssh -L 8080:192.168.20.56:2402 -p 2056 -t administrator@58.186.80.21 -N
```
- Access ```http://localhost:8080/``` on the web browser.
## Architecture
    .
    ├── ...
    ├── agent                           # Rainbow Agent  
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


## Database Architecture:
![img.png](img.png)

## Run Rainbow agent
```
python main.py --game pong --model "agent/results/pong/model.pth" --architecture data-efficient --hidden-size 256 --insert_obs --evaluate 
```