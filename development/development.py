import os
import subprocess

def install_packages():
    # Install necessary packages
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "nginx", "nodejs", "npm"])

def configure_nginx():
    # Create Nginx configuration
    nginx_config = f"""
    server {{
        listen 80;
        server_name localhost;

        location / {{
            proxy_pass http://127.0.0.1:3000;  # Adjust port if needed
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }}

        location /static {{
            alias {os.path.abspath('wsl-nodejs/public')};  # Adjust path
        }}
    }}
    """
    # Write configuration to file
    nginx_config_path = "/etc/nginx/sites-available/default"
    with open(nginx_config_path, "w") as f:
        f.write(nginx_config)
    print(f"Nginx configuration written to: {nginx_config_path}")

def start_services():
    # Start Nginx and Node.js development server
    subprocess.run(["sudo", "systemctl", "start", "nginx"])
    print("Nginx service started.")

def main():
    application_directory = "/home/idsithija/Projects/wsl-nodejs"  # Update with the correct path
    os.chdir(application_directory)  # Move to the application directory
    install_packages()
    configure_nginx()
    start_services()

if __name__ == "__main__":
    main()
