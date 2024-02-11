import subprocess

def install_pm2():
    subprocess.run(['npm', 'install', '-g', 'pm2'], check=True)

def install_nginx():
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'install', 'nginx'], check=True)

def configure_nginx(port):
    nginx_config = f"""
server {{
    listen 80;
    server_name localhost;

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
}}
"""
    with open('/etc/nginx/sites-available/default', 'w') as f:
        f.write(nginx_config)

    subprocess.run(['sudo', 'nginx', '-t'], check=True)
    subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)

def main():
    install_pm2()
    install_nginx()
    
    port = input("Enter the port assigned to your Node.js application by pm2: ")
    configure_nginx(port)

if __name__ == "__main__":
    main()
