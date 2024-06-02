<h1>This is a Grocery App</h1>
<h5>Follow these steps to setup the application</h5> 

<h3>Always remember to restart the servers if something's not working...</h3>

# Backend

For Installing Mailhog,
1. sudo apt-get -y install golang-go
2. sudo apt-get install git
3. go install github.com/mailhog/MailHog@latest
4. To run MailHog on Ubuntu -> ~/go/bin/MailHog
5. To access the Mailhog UI, go to -> http://localhost:8025/

To create a Virtual Environment,
1. python3 -m venv myenv
2. To activate -> source myenv/bin/activate
3. To deactivate -> deactivate

To Run Celery worker,
1. celery -A app.celery worker --loglevel=info [Do not forget to go to the backend file first... That's where your app.py exists]

To Run Celery beat,
1. celery -A app.celery beat --loglevel=info [Do not forget to go to the backend file first... That's where your app.py exists]

To Run Redis Server,
1. redis-server

To Run Python Backend Server,
1. python app.py [Do not forget to go to the backend file first... That's where your app.py exists]

To Run Vue Frontend Server,
1. vue serve [Run it on the normal cmd portal and not the linux env cause npm is not in venv]

To Download all the requirements from requirements.txt,
1. pip install -r requirements.txt

# Frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


