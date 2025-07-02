import subprocess
import os
import shutil
from dotenv import load_dotenv
from openai import OpenAI #when open ai api is use
from google import genai #when gimini api is use


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
        print("➡️  Type -> add <- for add all file in git\n")
        print("➡️  Type -> status <- for check status of git\n")
        print("➡️  Type -> C&P <- for commit and push to github\n")
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
                cwd = input("➡️  you are working with current working directory? y/n => ").strip().lower()
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
                add = input("➡️  you Want to add all files? y/n => ").strip().lower()
                if(add=='y'):
                    result = run_command(["git","add","."],cwd = os.getcwd())
                    if result:
                        print("✅  git add success")
                    else:
                        print("❌ Error running check cwd")
                else:
                    file = input("➡️  Enter file name => ").strip().lower()
                    while True:
                        result = run_command(["git","add",file],os.getcwd())
                        if result:
                            print("✅  git add success", file)
                        else:
                            print("❌ Error running check cwd")
                        adds = input("➡️  Want to add one more file y/n => ").strip().lower()
                        if (adds=='n'):
                            break

            # Ask status
            case "status":
                que = input("➡️  want to check status of cwd y/n => ")
                if(que=='y'):
                    result = run_command(["git","status"],cwd = os.getcwd())
                    if result:
                        print("✅  git status success")
                    else:
                        print("❌ Error running check cwd")
                else:
                    status = input("➡️ Enter path of folder to check status => ")
                    result = run_command(["git","status"],cwd = status)
                    if result:
                        print("✅  git status success")
                    else:
                        print("❌ Error running check cwd")
            
            #ask commit msg and commit
            case "c&p":
                load_dotenv()
                result = run_command(["git","add","."],cwd = os.getcwd())
                if result:
                    print("✅  git add success")
                else:
                    print("❌ Error running check cwd")
#generating commit from gimini
                limit_lines = 100
                result = subprocess.run( ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, encoding="utf-8", errors="replace")
                diff = result.stdout.strip().splitlines()

                if len(diff) > limit_lines:
                    diff = diff[:limit_lines]
                    diff.append("... [diff truncated]")

                diff_text = "\n".join(diff)

                prompt = f"""You are an assistant that writes helpful Git commit messages not do much process just analys this different and give a normal commit message.

                    Here is a git diff of staged changes:

                    {diff_text}

                    Write a concise, meaningful commit message: """
                
                client = genai.Client()
                try:
                    print("📝 Wait for Commit msg")
                    response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                    )

                    message = response.text.strip()
                    print(f"\n🤖 Suggested Commit Message:📝 {message}\n")
                except Exception as e:
                    print(e)

                confirm = input("✅ Use this message? (y/n): ").strip().lower()

                if(confirm == 'y'):
                    pass
                else:
                    message = input("📝 Enter commit message: ").strip()
                result = run_command(["git", "commit", "-m", message], cwd=os.getcwd())
                if result:
                    print("✅ Commit successful.")
                    result = run_command(["git","push"])
                    if(result):
                        print("✅ Push successful.")
                    else:
                        print("❌ Push failed. Did you forget to `commit` files?")
                else:
                    print("❌ Commit failed. Did you forget to `add` files?")



#   open ai commit code

#                 api_key = os.getenv("OPENAI_API_KEY")
#                 result = run_command(["git","add","."],cwd = os.getcwd())
#                 if result:
#                     print("✅  git add success")
#                 else:
#                     print("❌ Error running check cwd")
# #generating commit from gpt
#                 limit_lines = 100
#                 result = subprocess.run( ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, encoding="utf-8", errors="replace")
#                 diff = result.stdout.strip().splitlines()

#                 if len(diff) > limit_lines:
#                     diff = diff[:limit_lines]
#                     diff.append("... [diff truncated]")

#                 diff_text = "\n".join(diff)

#                 prompt = f"""You are an assistant that writes helpful Git commit messages not do much process just analys this different and give a normal commit messag.

#                     Here is a git diff of staged changes:

#                     {diff_text}

#                     Write a concise, meaningful commit message: """
                
#                 client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#                 try:
#                     response = client.chat.completions.create(
#                         model="gpt-3.5-turbo",
#                         messages=[
#                             {"role": "user", "content": prompt}
#                         ],
#                         temperature=0.4,
#                         max_tokens=100,
#                     )
#                     message = response["choices"][0]["message"]["content"].strip()
#                     print(f"\n🤖 Suggested Commit Message:\n\n📝 {message}\n")
#                 except Exception as e:
#                     pass

#                 confirm = input("✅ Use this message? (y/n): ").strip().lower()

#                 if(confirm == 'y'):
#                     pass
#                 else:
#                     message = input("📝 Enter commit message: ").strip()
#                 result = run_command(["git", "commit", "-m", message], cwd=os.getcwd())
#                 if result:
#                     print("✅ Commit successful.")
#                     result = run_command(["git","push"])
#                     if(result):
#                         print("✅ Push successful.")
#                     else:
#                         print("❌ Push failed. Did you forget to `commit` files?")
#                 else:
#                     print("❌ Commit failed. Did you forget to `add` files?")

            # exit from repo
            case "exit":
                print("✅ Done. Exiting Git Agent.")
                break
            case _:
                print("❌ Not avalable feature check input")


    
if __name__ == "__main__":
    if(git==1):
        main()