from cov.models import project as projectModel

def getProjectChoices():
    Obj = projectModel.objects.filter(deleted=0).order_by('-id')
    choicesId = [(tag.id, str(tag.id)+'/'+tag.projectName) for tag in Obj]
    return choicesId

def getProjectName(id):
    Obj = projectModel.objects.filter(id=id).order_by('-id')
    projectName =  Obj[0].projectName
    return projectName