# A puppet manifest that sets up my web servers for the deployment of web_static.
# Install Nginx if it not already installed.
# Create necessary directories if they don't exist.
# Set up the folder ownership and permissions.
# Create a fake HTML file to test nginx configuration.
# Set up nginx server block configuration to serve the content.

$nginx_setup = "server {
  listen 80 default_server;
  listen [::]:80 default_server;
  add_header X-Served-By ${hostname};
  root   /var/www/html;
  index  index.html index.htm;

  location /hbnb_static/ {
    alias /data/web_static/current/;
    index index.html index.htm;
  }

  location /redirect_me {
    return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
  }

  error_page 404 /404.html;
  location /404 {
    root /var/www/html;
    internal;
  }
}"

# Install Nginx
package { 'nginx':
  ensure  => 'installed',
}

# Create necessary directories
file { '/data/web_static/releases/test/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/shared/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => '<html>
  <head>
  </head>
  <body>
    Hello!
  </body>
</html>',
}

# Create the symbolic link /data/web_static/releases/test/ /data/web_static/current
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Set up nginx server block configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => $nginx_setup
}

# Restart Nginx
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
