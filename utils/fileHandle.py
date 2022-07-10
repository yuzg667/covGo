import os

# 获取当前文件夹下的文件名list
def getXmlFileName(file_dir):
    xmlFileList = []
    for root, dirs, files in os.walk(file_dir):
        #备注root返回当前目录路径；dirs返回当前路径下所有子目录；files返回当前路径下所有非目录子文件
        # return root,dirs,files
        for file in files:
            if str(file).endswith(".xml"):
                xmlFileList.append(str(file))
        return xmlFileList

# ss = getXmlFileName('../test123')
# print(ss)