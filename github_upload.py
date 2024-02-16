import os

def upload_github():
    os.system('git add .')
    os.system('git commit -m "Video change"')
    os.system('git push')
    print("upload success")

upload_github()
