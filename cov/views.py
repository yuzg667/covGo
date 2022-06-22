from django.shortcuts import render

# Create your views here.
# django启动时执行
from utils.execCmd import execCmd
from django.conf import settings
def initFileAndDir():
    execCmd(f'''mkdir -p {settings.BASE_DIR}/../covFilesDir''')
    execCmd(f'''chmod 777 {settings.BASE_DIR}/../covFilesDir/*''')
    execCmd(f'''chmod 777 {settings.BASE_DIR}/cmdTools''')
    execCmd(f'''chmod 777 {settings.BASE_DIR}/cmdTools/*''')
initFileAndDir()