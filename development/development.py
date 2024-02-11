import subprocess
import sys

def install_node():
    try:
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'nodejs'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'npm'], check=True)
        print("Node.js and npm installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install Node.js and npm: {e}")
        sys.exit(1)

def install_pm2():
    try:
        subprocess.run(['npm', 'install', '-g', 'pm2'], check=True)
        print("pm2 installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install pm2: {e}")
        sys.exit(1)

def install_nginx():
    try:
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'nginx'], check=True)
        print("Nginx installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install Nginx: {e}")
        sys.exit(1)

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
    try:
        with open('/etc/nginx/sites-available/default', 'w') as f:
            f.write(nginx_config)

        subprocess.run(['sudo', 'nginx', '-t'], check=True)
        subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
        print("Nginx configured successfully.")
    except Exception as e:
        print(f"Error: Failed to configure Nginx: {e}")
        sys.exit(1)

def main():
    install_node()
    install_pm2()
    install_nginx()
    
    port = input("Enter the port assigned to your Node.js application by pm2: ")
    configure_nginx(port)

if __name__ == "__main__":
    main()
