import os

def upload_github():
    os.system('git pull')
    os.system('git add .')
    os.system('git commit -m "Video change"')
    os.system('git push -u origin da0')
    print("upload success")

upload_github()
