import subprocess
import os

git_exe = r"C:\Users\yorman\AppData\Local\Programs\Git\cmd\git.exe"

def run_git(args):
    print("Running: git", " ".join(args))
    res = subprocess.run([git_exe] + args, capture_output=True, text=True, cwd=os.getcwd())
    print("STDOUT:", res.stdout.strip())
    if res.stderr.strip():
        print("STDERR:", res.stderr.strip())
    print("RETURN CODE:", res.returncode)
    return res.returncode == 0

# 1. Config user
run_git(["config", "user.name", "Lic. Yorman Trabasilo"])
run_git(["config", "user.email", "yormanantonio9@hotmail.com"])

# 2. Ensure main branch
run_git(["branch", "-M", "main"])

# 3. Git status before add
run_git(["status", "--short"])

# 4. Git add .
run_git(["add", "."])

# 5. Git status after add
run_git(["status", "--short"])

# 6. Commit
run_git(["commit", "-m", "feat: lanzamiento web oficial v2.0 Lic. Yorman Trabasilo"])
