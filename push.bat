@echo off
"C:\Program Files\Git\git-bash.exe" -c "echo last_modified = \\\"$(date +\"%%Y-%%m-%%d %%H:%%M:%%S\")\\\" > version.py"

"C:\Program Files\Git\git-bash.exe" -c "git add . && git commit -m \"Automated commit by bot: $(date)\" && git push origin master"
