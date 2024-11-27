import subprocess
import sys

def ensure_library_installed(library_name):
    """
    Ensure the required library is installed and up-to-date.
    :param library_name: str, the name of the library.
    """
    try:
        # Check if the library is installed by using pip show
        installed_version = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', library_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if installed_version.returncode == 0:
            # If installed, attempt to update it
            print(f"{library_name} is already installed. Checking for updates...")
            update_result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--upgrade', library_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if update_result.returncode == 0:
                print(f"{library_name} is up-to-date or successfully updated.")
            else:
                print(f"Failed to update {library_name}. Error:\n{update_result.stderr}")
        else:
            # If not installed, install it
            print(f"{library_name} is not installed. Installing now...")
            install_result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', library_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if install_result.returncode == 0:
                print(f"{library_name} successfully installed.")
            else:
                print(f"Failed to install {library_name}. Error:\n{install_result.stderr}")
    except Exception as e:
        print(f"An error occurred while ensuring {library_name} is installed: {e}")

# Main function
def main():
    ensure_library_installed("Skyfield")
    ensure_library_installed("Mathplotlib")
    ensure_library_installed("Numpy")
    ensure_library_installed("datetime")

    # Run the main code
    print("Hello World")

if __name__ == "__main__":
    main()
