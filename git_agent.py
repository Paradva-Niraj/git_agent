import subprocess
import os

def run_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Error running: {' '.join(command)}")
    return result.returncode == 0

def main():

    value = "welcome"
    print("\n🧠 Welcome to Git Agent")
    while(1):
        print("=======================================================================")
        print("➡️  Type clone for clone a repo\n")
        print("➡️  Type pull for pull latest commit\n")
        print("➡️  Type Exit for exit from agent\n")
        value = input("➡️  Enter your Request => ").strip().lower()
        match value:
            # Ask to clone repo
            case "clone":
                repo_url = input("🔗 Enter GitHub repo URL: ").strip()
                folder = repo_url.split('/')[-1].replace(".git", "")
                if os.path.exists(folder):
                    print("=======================================================================")
                    print("📁 Repo already exists locally.")
                    print("=======================================================================")
                else:
                    print("📥 Cloning...")
                    result = run_command(["git", "clone", repo_url])
                    if result: 
                        print("=======================================================================")
                        print("✅  Repo Clone success")
                        print("=======================================================================")
                    else:
                        print("=======================================================================")
                        print("❌ Error running check repo url")
                        print("=======================================================================")

            # Ask to pull repo
            case "pull":
                repo_name = input("📁 Enter local folder name of repo: ").strip()
                if os.path.exists(repo_name):
                    print("🔄 Pulling latest changes...")
                    result = run_command(["git", "pull"], cwd=repo_name)
                    if result:
                        print("=======================================================================")
                        print("🔄 Pulling latest changes complited")
                        print("=======================================================================")
                    else:
                        print("=======================================================================")                            
                        print(" ❌ Error running:")
                        print("=======================================================================")    
                else:
                    print("=======================================================================")
                    print("⚠️ Folder not found. Clone the repo first.")        
                    print("=======================================================================")
            
            # exit from repo
            case "exit":
                print("✅ Done. Exiting Git Agent.")
                break
            case _:
                print("❌ Not avalable feature check input")


    
if __name__ == "__main__":
    main()