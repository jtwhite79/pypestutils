import os
import shutil
org_d = os.path.join("docs","pypestutils")
if os.path.exists(org_d):
    shutil.rmtree(org_d)
os.system("pdoc --html --output-dir docs pypestutils")

for f in os.listdir(org_d):
    dest_f = os.path.join("docs",f)
    if os.path.exists(dest_f):
        os.remove(dest_f)
    shutil.copy2(os.path.join(org_d,f),dest_f)
