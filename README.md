sudo apt update <br />
sudo apt upgrade -y <br />
sudo apt install nginx <br />
sudo /etc/init.d/nginx start <br />
cd /home <br />
sudo git clone https://github.com/milgo/vue-flask-fbd-editor.git <br />
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
location /program {<br />
	proxy_pass http://localhost:5000/program <br />
}<br />
location /start {<br />
	proxy_pass http://localhost:5000/start <br />
}<br />
location /stop {<br />
	proxy_pass http://localhost:5000/stop <br />
}<br />
---------------------------------------<br />
restart nginx: sudo systemctl restart nginx<br />
status nginx: sudo systemctl status nginx<br />
