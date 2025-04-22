from MayaUtils import *
from PySide2.QtWidgets import QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout

def TryAction(actionFunc):
    def wrapper(*args, **kwargs):
        try:
            actionFunc(*args, **kwargs)
        except Exception as e:
            QMessageBox().critical(None, "Error!", f"{e}")

    return wrapper

class AnimClip:
    def __init__(self):
        self.subfix = ""
        self.frameMin = mc.playbackOptions(q = True, min = True)
        self.frameMax = mc.playbackOptions(q = True, max = True)
        self.shouldExport = True
        
class MayaToUE:
    def __init__(self):
        self.rootJnt = ""
        self.models = set()
        self.animaions : list[AnimClip] = []
        self.fileName = ""
        self.saveDir = ""
    def AddSelectedMeshes(self):
        selection = mc.ls(sl = True)

        if not selection:
            raise Exception("No Mesh Selected, please select all the meshes of your rig")
        
        meshes = []
        for sel in selection:
            if IsMesh(sel):
                meshes.append(sel)

        if len(meshes) == 0:
            raise Exception("No Mesh Selected, please select all the meshes of your rig")
        
        self.models = meshes


    def AddRootJoint(self):
        if not self.rootJnt:
            raise Exception("No Root Joint Assigned, please set the root joint of your rig first")
        
        if mc.objExists(self.rootJnt):
            currentRootPos = mc.xform(self.rootJnt, q = True, ws = True, t = True)
            if currentRootPos[0] == 0 and currentRootPos[1] == 0 and currentRootPos[2] == 0:
                raise Exception("Current root joint is at origin already, no need to make a new one!")
            
        mc.select(cl = True)
        rootJntName = self.rootJnt + "_root"
        mc.joint(n = rootJntName)
        mc.parent(self.rootJnt, rootJntName)
        self.rootJnt = rootJntName


    def SetSelectedJointAsRoot(self):
        selection = mc.ls(sl = True, type = "joint")
        if not selection:
            raise Exception("Wrong Selection, Please select the root joint of your rig!")
        
        self.rootJnt = selection[0]


class MayaToUEWidget(MayaWindow):
    def GetWidgetUniqueName(self):
        return "MayaToUEWidgetJL4172025407"
    
    def __init__(self):
        super().__init__()
        self.mayaToUE = MayaToUE()

        self.setWindowTitle("Maya to UE")
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.rootJntText = QLineEdit()
        self.rootJntText .setEnabled(False)
        self.masterLayout.addWidget(self.rootJntText)

        setSelectedAsRootJntBtn = QPushButton("Set Root Joint")
        setSelectedAsRootJntBtn.clicked.connect(self.setSelectedAsRootJntBtnClicked)
        self.masterLayout.addWidget(setSelectedAsRootJntBtn)

        addRootJntBtn = QPushButton("Add Root Joint")
        addRootJntBtn.clicked.connect(self.AddRootJntBtnClicked)
        self.masterLayout.addWidget(addRootJntBtn)

        self.meshList = QListWidget()
        self.masterLayout.addWidget(self.meshList)
        self.meshList.setMaximumHeight(100)

        addMeshesBtn = QPushButton("Add Meshes")
        addMeshesBtn.clicked.connect(self.AddMeshesBtnClicked)
        self.masterLayout.addWidget(addMeshesBtn)

    @TryAction
    def AddMeshBtnClicked(self):
        self.mayaToUE.AddSelectedMeshes()
        self.meshList.clear()
        self.meshList.addItems(self.mayaToUE.models)

    @TryAction
    def AddRootJntBtnClicked(self):
        self.mayaToUE.AddRootJoint()
        self.rootJntText.setText(self.mayaToUE.rootJnt)

    @TryAction
    def setSelectedAsRootJntBtnClicked(self):
        self.mayaToUE.SetSelectedJointAsRoot()
        self.rootJntText.setText(self.mayaToUE.rootJnt)

MayaToUEWidget().show()