import subprocess

def get_available_updates():
    
    result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]  
    
    packages = []
    for line in lines:
        package_name = line.split("/")[0]  # Extract package name before the first "/"
        packages.append(package_name)
    
    return packages


def install_updates(packages):
    
    for package in packages:
        print(f"Installing: {package} ...")
        status = subprocess.run(["sudo", "apt", "install", "-y", package])
        
        if status.returncode == 0:
            print(f"{package} updated successfully.")
        else:
            print(f"Failed to update {package}.")


def main():
    
    packages = get_available_updates()
    
    if packages == []:
        print("No updates available.")
        return


    print("Available Updates:")
    index = 1
    for package in packages:
        print(f"{index}. {package}")
        index += 1

    print("\nOptions:---------------------")
    print("1. Update all packages")
    print("2. Update a specific package")

    choice = input("Enter your choice: ")

    if choice == "1":
        install_updates(packages)
        
    elif choice == "2":
        
        package_index = input("Enter package index number to update: ")
        
        if package_index.isdigit():
            package_index = int(package_index) # typecasting
            
            if 1 <= package_index <= len(packages):
                install_updates([packages[package_index - 1]])
            else:
                print("Invalid index number.")
                
        else:
            print("Invalid input.")
            
    else:
        print("Invalid choice, either update all or select one's index to update .")




if __name__ == "__main__":
    main()