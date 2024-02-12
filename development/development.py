import subprocess
import sys
import os

def install_node():
    try:
        # Step 1: Running 'sudo apt update'
        subprocess.run(['sudo', 'apt', 'update'], check=True)

        # Step 2: Installing Node.js
        subprocess.run(['sudo', 'apt', 'install', '-y', 'nodejs'], check=True)

        # Step 3: Installing npm
        subprocess.run(['sudo', 'apt', 'install', '-y', 'npm'], check=True)

        # Printing success message
        print("Node.js and npm installed successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to install Node.js and npm: {e}")
        sys.exit(1)

def main():
    # Calling the function to install Node.js and npm
    install_node()

if __name__ == "__main__":
    # Calling the main function
    main()
