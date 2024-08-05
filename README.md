
sudo apt update <br />
sudo apt install nginx <br />
sudo /etc/init.d/nginx start <br />
git clone https://github.com/milgo/vue-flask-fbd-editor.git <br />
sudo cp -rfa ./vue-flask-fbd-editor/dist/. /var/www/html/ <br />
sudo rm index.nginx-debian.html <br />