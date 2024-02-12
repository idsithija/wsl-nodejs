import subprocess
import sys

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
        # Changing directory to your Node.js application directory
        subprocess.run(['cd', '/path/to/your/username/Projects/wsl-nodejs'], check=True)

        # Installing Node.js modules using npm
        subprocess.run(['npm', 'install'], check=True)

        # Printing success message
        print("Node modules installed successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to install Node modules: {e}")
        sys.exit(1)

def main():
    # Calling the function to update Node.js
    update_node()

    # Calling the function to install Nginx
    install_nginx()

        # Calling the function to install PM2
    install_pm2()

if __name__ == "__main__":
    # Calling the main function
    main()
