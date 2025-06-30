import subprocess
import os
import shutil

#check git is install or not if not intall that
git = 0
if shutil.which("git"):
    git = 1
    # print("Git is installed!")
else:
    print("Git is NOT installed. Please install it first.")

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
        print("➡️  Type -> clone <- for clone a repo\n")
        print("➡️  Type -> pull <- for pull latest commit\n")
        print("➡️  Type -> add <- for add all file in github\n")
        print("➡️  Type -> Exit <- for exit from agent\n")
        value = input("➡️  Enter your Request => ").strip().lower()
        match value:
            # Ask to clone repo
            case "clone":
                repo_url = input("🔗 Enter GitHub repo URL: ").strip()
                folder = repo_url.split('/')[-1].replace(".git", "")
                if os.path.exists(folder):
                    print("📁 Repo already exists locally.")
                else:
                    print("📥 Cloning...")
                    result = run_command(["git", "clone", repo_url])
                    if result:
                        print("✅  Repo Clone success")
                    else:
                        print("❌ Error running check repo url")

            # Ask to pull repo
            case "pull":
                cwd = input("➡️  you are working with current working directory? y/n => ")
                if(cwd=='y'):
                    repo_name = os.getcwd()
                else:
                    repo_name = input("📁 Enter local folder path of repo: ").strip()
                if os.path.exists(repo_name):
                    print("\n🔄 Pulling latest changes...")
                    result = run_command(["git", "pull"], cwd=repo_name)
                    if result:
                        print("🔄 Pulling latest changes complited")
                    else:
                        print(" ❌ Error running:")
                else:
                    print("⚠️ Folder not found. Clone the repo first.")    

            # Ask for Add files in git
            case "add":
                add = input("➡️  you Want to add all files? y/n => ")
                if(add==1):
                    result = run_command(["git add","."],cwd = os.getcwd())
                    if result:
                        print("✅  git add success")
                    else:
                        print("❌ Error running check cwd")
                else:
                    file = input("➡️  Enter file name => ")
                    while True:
                        result = run_command(["git","add",file],os.getcwd())
                        if result:
                            print("✅  git add success", file)
                        else:
                            print("❌ Error running check cwd")
                        adds = input("➡️  Want to add one more file y/n => ")
                        if (adds=='n'):
                            break
                

                
            # exit from repo
            case "exit":
                print("✅ Done. Exiting Git Agent.")
                break
            case _:
                print("❌ Not avalable feature check input")


    
if __name__ == "__main__":
    if(git==1):
        main()