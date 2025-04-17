from MayaUtils import *
from PySide2.QtWidgets import QVBoxLayout

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

class MayaToUEWidget(MayaWindow):
    def GetWidgetUniqueName(self):
        return "MayaToUEWidgetJL4172025407"
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maya to UE")
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

MayaToUEWidget().show()