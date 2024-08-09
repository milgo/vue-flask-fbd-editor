
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
sudo apt install python3-flask-cors 
sudo apt install python3-waitress
sudo systemctl daemon-reload
sudo systemctl start program-data-server.service
sudo systemctl enable program-data-server.service