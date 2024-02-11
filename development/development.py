import subprocess

def install_nodejs():
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "nodejs"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "npm"], check=True)
        print("Node.js and npm installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    install_nodejs()
