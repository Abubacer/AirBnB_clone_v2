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

package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
  require  => Exec['create_web_static_dir'],
}

file { '/var/www':
  ensure  => 'directory',
  mode    => '0755',
  recurse => true,
}

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Hello World!\n",
}

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
}

exec { 'create_web_static_dir':
  command => 'mkdir -p /data/web_static/releases/test /data/web_static/shared',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Package['nginx'],
}

file { '/data/':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Hello!\n",
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  mode    => '0644',
  content => $nginx_setup,
}

exec { 'create_symbolic_link':
  command => "ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'",
  path    => '/usr/bin:/usr/sbin:/bin',
  require => File['/etc/nginx/sites-available/default'],
}

exec { 'nginx restart':
  command => 'sudo service nginx restart',
  path    => '/usr/bin:/usr/sbin:/bin',
  
}
