#### Instalation (on Raspberry PI)
Open terminal or connect using remote ssh session and run commands:
- sudo apt update <br />
- sudo apt upgrade -y <br />
- sudo apt install nginx <br />
- sudo /etc/init.d/nginx start <br />
- cd /home <br />
- sudo git clone https://github.com/milgo/vue-flask-fbd-editor.git <br />
- sudo rm -r /var/www/html/* <br />
- sudo cp -rfa ./vue-flask-fbd-editor/dist/. /var/www/html/ <br />
- sudo cp -f ./vue-flask-fbd-editor/backend/program-data-server.service /etc/systemd/system/ <br />
- sudo rm /var/www/html/index.nginx-debian.html <br />
- sudo apt install python3 python3-flask python3-pip <br />
- sudo apt install python3-flask-cors <br />
- sudo apt install python3-waitress <br />
- sudo systemctl daemon-reload <br />
- sudo systemctl start program-data-server.service <br />
- sudo systemctl enable program-data-server.service <br />
- sudo nano /etc/nginx/sites-available/default. In server section of this file add lines as follows: <br />
```md
location /status {
	proxy_pass http://localhost:5000/status;
}<br />
location /project {
	proxy_pass http://localhost:5000/project;
}
location /start {
	proxy_pass http://localhost:5000/start;
}
location /stop {
	proxy_pass http://localhost:5000/stop;
}
location /monitor {
	proxy_pass http://localhost:5000/monitor;
}
location /variables {
	proxy_pass http://localhost:5000/variables;
}
location /compile {
	proxy_pass http://localhost:5000/compile;
}
location /pullruntimedata {
	proxy_pass http://localhost:5000/pullruntimedata;
}
location /forcevariables {
	proxy_pass http://localhost:5000/forcevariables;
}
```

#### Development
Assuming nodejs is installed with vite and python with flask on desktop computer (Windows):
- Change line in App.vue: 'const flaskURL = "http://192.168.1.2"' to 'const flaskURL = "http://localhost:5000"'
- Run dev.bat to run vue frontend
- Run backend/run.bat to run flask backend 

#### Build
- Change line in App.vue: 'const flaskURL = "http://localhost:5000"' to 'const flaskURL = "http://192.168.1.2"'
- Run build.bat
- Git commit changes with message "uploading dist vx.x"

#### Deploy new build on device
Open terminal or connect using remote ssh session and run commands:
- git pull origin main
- delete fake library gpiozero.py file
- run sudo rm -r /var/www/html/*
- sudo cp -rfa /home/vue-flask-fbd-editor/dist/. /var/www/html/
- *Before running new build on device make sure to clear files project.json, variables.json, listing.json by rewriting them with "[]" value (without quotation marks - python empty array)
- sudo systemctl daemon-reload
- sudo systemctl restart nginx
- sudo systemctl restart program-data-server.service
-  sudo systemctl status nginx

#### Setup direct Ethernet connection
TODO

#### Runtime data description
RLO - runtime data (id -> value) of all function blocks<br />
{<br />
    "13123322" : "True",<br />
    "32423445" : "243",<br />
    ...<br />
}<br />
<br />
THIS - current listing block<br />
{<br />
    "functionName": "before_AND_INPUT", //function to be executed<br />
    "inputId": "1736893940672", //input id of parent node to which is connected<br />
    "memoryAddr": "%i1", //memory associated to current function<br />
    "inputName": "name", //input name of input node to which is connected<br />
    "childId": "1736893945336", //id of input node to which is connected<br />
    "id": "1736893939333" //id of current node block<br />
}<br />
<br />
MEM= { <br />
    "name1" : {<br />
        "type": "bool", //variable type<br />
        "value": "1", //variable value<br />
        "forced": "False", //is it forced<br />
        "forcedValue": "False", //forced value<br />
    }, <br />
    "name2" : <br />
        { ... }<br />
---------------------------------------<br />
