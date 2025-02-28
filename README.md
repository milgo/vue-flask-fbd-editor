Vue developement is done in windows so in that case we add :5000 port option to flask backend in App.vue file axios requests. <br />
In order to proprely build app for raspberry pi just before build we need to remove those port numbers because we proxy pass them in nginx.

#### Instalation (on raspbery PI)
sudo apt update <br />
sudo apt upgrade -y <br />
sudo apt install nginx <br />
sudo /etc/init.d/nginx start <br />
cd /home <br />
sudo git clone https://github.com/milgo/vue-flask-fbd-editor.git <br />
sudo rm -r /var/www/html/* <br />
sudo cp -rfa ./vue-flask-fbd-editor/dist/. /var/www/html/ <br />
sudo cp -f ./vue-flask-fbd-editor/backend/program-data-server.service /etc/systemd/system/ <br />
sudo rm /var/www/html/index.nginx-debian.html <br />
sudo apt install python3 python3-flask python3-pip <br />
sudo apt install python3-flask-cors <br />
sudo apt install python3-waitress <br />
sudo systemctl daemon-reload <br />
sudo systemctl start program-data-server.service <br />
sudo systemctl enable program-data-server.service <br />
sudo nano /etc/nginx/sites-available/default -> in server section add: <br />
````md
location /status {<br />
	proxy_pass http://localhost:5000/status; <br />
}<br />
location /project {<br />
	proxy_pass http://localhost:5000/project; <br />
}<br />
location /start {<br />
	proxy_pass http://localhost:5000/start; <br />
}<br />
location /stop {<br />
	proxy_pass http://localhost:5000/stop; <br />
}<br />
location /monitor {<br />
	proxy_pass http://localhost:5000/monitor; <br />
}<br />
location /variables {<br />
	proxy_pass http://localhost:5000/variables; <br />
}<br />
location /compile {<br />
	proxy_pass http://localhost:5000/compile;<br />
}<br />
location /pullruntimedata {<br />
	proxy_pass http://localhost:5000/pullruntimedata;<br />
}<br />
location /forcevariables {<br />
	proxy_pass http://localhost:5000/forcevariables;<br />
}<br />
````md

#### Development:<br />
Assuming nodejs is installed with vite and python with flask on desktop computer (Windows):
- Change line in App.vue: 'const flaskURL = "http://192.168.1.2"' to 'const flaskURL = "http://localhost:5000"'
- Run dev.bat to run vue frontend
- Run backend/run.bat to run flask backend 

#### Build:<br />
- Change line in App.vue: 'const flaskURL = "http://localhost:5000"' to 'const flaskURL = "http://192.168.1.2"'
- Run build.bat
- Git commit changes with message "uploading dist vx.x"

#### Deploy new build on device:<br />
- Run "git pull origin main"
- Run "delete fake library gpiozero.py file"
- Run "run sudo rm -r /var/www/html/*"
- Run "sudo cp -rfa /home/vue-flask-fbd-editor/dist/. /var/www/html/"
- Before running new build on device make sure to clear files project.json, variables.json, listing.json by rewriting them with "[]" value (without quotation marks - python empty array)
- Run "sudo systemctl daemon-reload"
- Restart nginx: sudo systemctl restart nginx<br />
- Restart nginx: sudo systemctl restart program-data-server.service<br />
- Status nginx: sudo systemctl status nginx<br />

#### Runtime data description:<br />
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
