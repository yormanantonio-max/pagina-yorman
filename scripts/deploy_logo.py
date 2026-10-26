import subprocess

git_exe = r"C:\Users\yorman\AppData\Local\Programs\Git\cmd\git.exe"

def run(cmd):
    print("Running:", " ".join(cmd))
    res = subprocess.run([git_exe] + cmd, capture_output=True, text=True)
    print("STDOUT:", res.stdout.strip())
    if res.stderr.strip():
        print("STDERR:", res.stderr.strip())
    print("EXIT:", res.returncode)
    return res.returncode == 0

run(["add", "."])
run(["commit", "-m", "feat: integracion del emblema oficial de marca en cabecera principal"])
run(["push", "origin", "main"])
