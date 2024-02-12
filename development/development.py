import subprocess
import sys
import os
import stat

# Define the application directory path as a global variable
node_app_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'Projects', 'wsl-nodejs'))

def update_node():
    try:
        # Running the curl command to add the NodeSource repository
        curl_process = subprocess.Popen(['curl', '-fsSL', 'https://deb.nodesource.com/setup_21.x'], stdout=subprocess.PIPE)

        # Piping the output of curl to bash with sudo permissions
        bash_process = subprocess.Popen(['sudo', '-E', 'bash', '-'], stdin=curl_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the processes to finish
        curl_process.stdout.close()
        out, err = bash_process.communicate()

        if bash_process.returncode != 0:
            # If an error occurred, print error message
            print(f"Error: Failed to update Node.js: {err.decode()}")
            sys.exit(1)

        # Installing Node.js from the NodeSource repository
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'], check=True)

        # Printing success message
        print("Node.js updated successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to update Node.js: {e}")
        sys.exit(1)

def install_nginx():
    try:
        # Installing Nginx
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nginx'], check=True)

        # Printing success message
        print("Nginx installed successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to install Nginx: {e}")
        sys.exit(1)

def install_pm2():
    try:
        # Installing PM2 globally
        subprocess.run(['sudo', 'npm', 'install', '-g', 'pm2'], check=True)

        # Printing success message
        print("PM2 installed successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to install PM2: {e}")
        sys.exit(1)

def install_node_modules():
    try:
        # Installing Node.js modules using npm in the directory containing the package.json file
        subprocess.run(['sudo', 'npm', 'install'], check=True, cwd=node_app_dir)

        # Printing success message
        print("Node modules installed successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to install Node modules: {e}")
        sys.exit(1)

def start_node_app_with_pm2():
    try:
        # Starting Node.js application with PM2
        subprocess.run(['/usr/lib/node_modules/pm2/bin/pm2', 'start', '-f', 'app.js'], check=True, cwd=node_app_dir)

        # Saving PM2 process list to persist through reboots
        subprocess.run(['/usr/lib/node_modules/pm2/bin/pm2', 'save'], check=True)

        # Generating startup script for PM2
        subprocess.run(['sudo', 'env', f'PATH=$PATH:/usr/bin', '/usr/lib/node_modules/pm2/bin/pm2', 'startup', 'systemd', '-u', 'idsithija', '--hp', f'/home/idsithija'], check=True)

        # Printing success message
        print("Node.js application started with PM2 and configured to start on system boot.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to start Node.js application with PM2: {e}")
        sys.exit(1)

def configure_nginx():
    try:
        # Open Nginx configuration file for editing with sudo
        nginx_conf_path = '/etc/nginx/sites-available/default'
        with open(nginx_conf_path, 'w') as file:
            file.write("""server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
""")

        # Testing Nginx configuration
        subprocess.run(['sudo', 'nginx', '-t'], check=True)

        # Reloading Nginx to apply changes
        subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)

        # Printing success message
        print("Nginx configuration updated successfully.")

    except FileNotFoundError:
        print("Error: Nginx configuration file not found.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to configure Nginx: {e}")
        sys.exit(1)

def main():
    # Calling the function to update Node.js
    update_node()

    # Calling the function to install Nginx
    install_nginx()

    # Calling the function to install PM2
    install_pm2()

    # Calling the function to install node_modules
    install_node_modules()

    # Starting the Node.js application with PM2 and configuring startup on system boot
    start_node_app_with_pm2()

    # configure nagix to show node app
    configure_nginx()

if __name__ == "__main__":
    # Calling the main function
    main()
