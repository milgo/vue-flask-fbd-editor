Vue developement is done in windows so in that case we add :5000 port option to flask backend in App.vue file axios requests. <br />
In order to proprely build app for raspberry pi just before build we need to remove those port numbers because we proxy pass them in nginx.

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
location /status {<br />
	proxy_pass http://localhost:5000/status <br />
}<br />
location /project {<br />
	proxy_pass http://localhost:5000/project <br />
}<br />
location /start {<br />
	proxy_pass http://localhost:5000/start <br />
}<br />
location /stop {<br />
	proxy_pass http://localhost:5000/stop <br />
}<br />
location /monitor {<br />
	proxy_pass http://localhost:5000/monitor <br />
}<br />
location /variables {<br />
	proxy_pass http://localhost:5000/variables <br />
}<br />
location /compile {<br />
	proxy_pass http://localhost:5000/compile<br />
}<br />
location /pullruntimedata {<br />
	proxy_pass http://localhost:5000/pullruntimedata<br />
}<br />
location /forcevariables {<br />
	proxy_pass http://localhost:5000/forcevariables<br />
}<br />
---------------------------------------<br />
<br />
/* !IMPORTANT 
	Before running new build on device make sure to clear files project.json, variables.json, listing.json by rewriting them with "[]" value (without quotation marks - python empty array)
*/
<br /><br />
Deply new build:<br />
---------------------------------------<br />
git pull origin main<br />
sudo cp -rfa ./vue-flask-fbd-editor/dist/. /var/www/html/ <br />
restart nginx: sudo systemctl restart nginx<br />
restart nginx: sudo systemctl restart program-data-server.service<br />
status nginx: sudo systemctl status nginx<br />
