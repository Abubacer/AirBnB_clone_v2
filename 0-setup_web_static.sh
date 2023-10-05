#!/usr/bin/env bash
# Sets up my web servers web-01 and web-02 for the deployment of AirBnB clone web_static.

# Install Nginx if it not already installed:
sudo apt-get update
sudo apt-get install -y nginx
# Create necessary directories if they don't exist:
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
# Create a fake HTML file to test nginx configuration:
echo "<html>
  <head>
  </head>
  <body>
    Hello!
  </body>
<html>" > /data/web_static/releases/test/index.html
# Create the symbolic link:
ln -sf /data/web_static/releases/test/ /data/web_static/current
# Set up the folder ownership and permissions:
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 755 /data/
# Set up nginx server block configuration to serve the content of /data/web_static/current/ to hbnb_static:
sudo sed -i '/listen 80 default_server/a   location \/hbnb_static {\n\talias /data/web_static/current;\n}' /etc/nginx/sites-available/default
# Restart Nginx to apply changes:
sudo service nginx restart
