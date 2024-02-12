import subprocess
import sys

def update_node():
    try:
        # Running the curl command to add the NodeSource repository
        subprocess.run(['curl', '-fsSL', 'https://deb.nodesource.com/setup_21.x', '|', 'sudo', '-E', 'bash', '-'], check=True)

        # Installing Node.js from the NodeSource repository
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'], check=True)

        # Printing success message
        print("Node.js updated successfully.")

    except subprocess.CalledProcessError as e:
        # Handling errors
        print(f"Error: Failed to update Node.js: {e}")
        sys.exit(1)

def main():
    # Calling the function to update Node.js
    update_node()

if __name__ == "__main__":
    # Calling the main function
    main()
