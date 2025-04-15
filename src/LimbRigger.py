from PySide2.QtGui import QColor
from PySide2.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget #Imports different things so we can use them in this file
from PySide2.QtCore import Qt, Signal # Imports Qt so that we can use it in this file
from maya.OpenMaya import MVector
import maya.OpenMayaUI as omui # imports maya UI as a smaller nickname to be used in the file
import maya.mel as mel
import shiboken2 # imports shibroken2

def GetMayaMainWindow()-> QMainWindow: # Defines a function called GetMayaMainWindow that uses QMainWindow
    mainWindow = omui.MQtUtil.mainWindow() # Makes the Maya UI main window equal the variable mainWindow so it's easier to use later
    return shiboken2.wrapInstance(int(mainWindow), QMainWindow) # returns the main window UI

def DeleteWidgetWithName(name): # Defines a function called DeleteWidgetWithName with the parameter name
    for widget in GetMayaMainWindow().findChildren(QWidget, name): # Creates a for loop that checks for widget in GetMayaMainWindow and finds children
        widget.deleteLater() # Deletes widget at a later time

class MayaWindow(QWidget): # Creates a class called MayaWindow that uses the parameters of QWidget
    def __init__(self): # Creates a constructor
        super().__init__(parent = GetMayaMainWindow()) # Calls to the parent class for inheritance and makes parent equal to GetMayaMainWindow
        DeleteWidgetWithName(self.GetWidgetUniqueName()) # Deletes widget with unique name
        self.setWindowFlags(Qt.WindowType.Window) # Creates a window flag for the Maya window that we made
        self.setObjectName(self.GetWidgetUniqueName()) # Names widget with unique name

    def GetWidgetUniqueName(self): # Defines a function called GetWidgetUniqueName with parameter self
        return "seujfedfehufhufhuhywe3djfcedhsuiafhdse" # returns a string to be the unique name

import maya.cmds as mc # Imports maya.cmds as a shorter nickname mc to use easier later on
class LimbRigger: # Creates a class called LimbRigger
    def __init__(self): # Creates a constructor
        self.root = "" # Initializes root as a string variable
        self.mid = "" # Initializes mid as a string variable
        self.end = "" # Initializes end as a string variable
        self.controllerSize = 5 # Initializes controllerSize as 5 and an integer
        self.controllerColor = [0, 0, 0]
    
    def FindJointBasedOnSelection(self): # Defines a function named FindJointBasedOnSelection with parameter self
        try: # tries to do whatever is below this
            self.root = mc.ls(sl=True, type="joint")[0] # Checks to make sure it is a joint and names it root
            self.mid = mc.listRelatives(self.root, c=True, type="joint")[0] # Checks to make sure it's a joint and names it mid
            self.end = mc.listRelatives(self.mid, c=True, type="joint")[0] # Checks to make sure it's a joint and names it end
        except Exception as e: # Makes an exception for when it is not able to name three joints/when the wrong joint was selected
            raise Exception(f"Wrong Selection, Please select the first joint of the limb!") # Tells person that what they did was wrong and they need to try again

    def CreateFKControllerForJoint(self, jntName): # Defines a function called CreateFKControllerForJoint with parameters self and jntName
        ctrlName = "ac_l_fk_" + jntName # Creates a variable that combines ac_l_fk_ and whatever the joint is named
        ctrlGrpName = ctrlName + "_grp" # Creates a variable that combines what is in the variable ctrlName plus _grp
        mc.circle(name = ctrlName, radius = self.controllerSize, normal = (1, 0, 0)) # Creates a circle shaped controller
        mc.group(ctrlName, n = ctrlGrpName) # Groups circle controller and names it the ctrlGrpName
        mc.matchTransform(ctrlGrpName, jntName) # Matches the circle controller to the joint
        mc.orientConstraint(ctrlName, jntName) # Constrains the circle controller to the joint
        return ctrlName, ctrlGrpName # returns variables ctrlName and ctrlGrpName
    
    def CreateBoxController(self, name):
        mel.eval(f"curve -n {name} -d 1 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;")
        mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
        mc.makeIdentity(name, apply = True) # Freeze Transformation
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
    
    def CreatePlusController(self, name):
        mel.eval(f"curve -n {name} -d 1 -p -9 0 9 -p -9 0 8 -p -8 0 8 -p -8 0 9 -p -7 0 9 -p -7 0 10 -p -8 0 10 -p -8 0 11 -p -9 0 11 -p -9 0 10 -p -10 0 10 -p -10 0 9 -p -9 0 9 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;")
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
    
    def GetObjectLocation(self, objectName):
        x, y, z = mc.xform(objectName, q = True, ws = True, t = True) # quires the translation of the object in the world space
        return MVector(x, y, z)
    
    def PrintMVector(self, vector):
        print(f"<{vector.x}, {vector.y}, {vector.z}>")
    
    def RigLimb(self): # Defines a function called RigLimb with the parameter self
        rootCtrl, rootCtrlGrp = self.CreateFKControllerForJoint(self.root) # Creates two variables that  use the FK controllers for the root joint
        midCtrl, midCtrlGrp = self.CreateFKControllerForJoint(self.mid) # Creates two variables that  use the FK controllers for the mid joint
        endCtrl, endCtrlGrp = self.CreateFKControllerForJoint(self.end) # Creates two variables that  use the FK controllers for the end joint

        mc.parent(midCtrlGrp, rootCtrl) # Parents the midCtrlGrp to the rootCtrl
        mc.parent(endCtrlGrp, midCtrl) # Parents the endCtrlGrp to the midCtrl

        ikEndCtrl = "ac_ik_" + self.end
        ikEndCtrl, ikEndCtrlGrp = self.CreateBoxController(ikEndCtrl)
        mc.matchTransform(ikEndCtrlGrp, self.end)
        endOrientConstraint = mc.orientConstraint(ikEndCtrl, self.end)[0]

        rootJntLoc = self.GetObjectLocation(self.root)
        self.PrintMVector(rootJntLoc)

        ikHandleName = "ikHandle_" + self.end
        mc.ikHandle(n=ikHandleName, sol = "ikRPsolver", sj = self.root, ee = self.end)

        poleVectorLocationVals = mc.getAttr(ikHandleName + ".poleVector")[0]
        poleVector = MVector(poleVectorLocationVals[0], poleVectorLocationVals[1], poleVectorLocationVals[2])
        poleVector.normal()

        endJntLoc = self.GetObjectLocation(self.end)
        rootToEndVector = endJntLoc - rootJntLoc

        poleVectorCtrlLoc = rootJntLoc + rootToEndVector / 2 + poleVector * rootToEndVector.length()
        poleVectorCtrl = "ac_ik_" + self.mid
        mc.spaceLocator(n=poleVectorCtrl)
        poleVectorCtrlGrp = poleVectorCtrl + "_grp"
        mc.group(poleVectorCtrl, n = poleVectorCtrlGrp)
        mc.setAttr(poleVectorCtrlGrp + " .t", poleVectorCtrlLoc.x, poleVectorCtrlLoc.y, poleVectorCtrlLoc.z, typ = "double3")

        mc.poleVectorConstraint(poleVectorCtrl, ikHandleName)

        ikfkBlendCtrl = "ac_ikfk_blend" + self.root
        ikfkBlendCtrl, ikfkBlendCtrlGrp = self.CreatePlusController(ikfkBlendCtrl)
        mc.setAttr(ikfkBlendCtrlGrp + ".t", rootJntLoc.x*2, rootJntLoc.y, rootJntLoc.z*2, typ = "double3")

        ikfkBlendAttrName = "ikfkBlend"
        mc.addAttr(ikfkBlendCtrl, ln = ikfkBlendAttrName, min = 0, max = 1, k= True )
        ikfkBlendAttr = ikfkBlendCtrl + "." + ikfkBlendAttrName

        mc.expression(s=f"{ikHandleName}.ikBlend ={ikfkBlendAttr}")
        mc.expression(s=f"{ikEndCtrlGrp}.v ={poleVectorCtrlGrp}.v={ikfkBlendAttr}")
        mc.expression(s=f"{rootCtrlGrp}.v=1-{ikfkBlendAttr}")
        mc.expression(s=f"{endOrientConstraint}.{endCtrl}W0 = 1- {ikfkBlendAttr}")
        mc.expression(s=f"{endOrientConstraint}.{ikEndCtrl}W1 = {ikfkBlendAttr}")

        topGrpName = f"{self.root}_rig_grp"
        mc.group([rootCtrlGrp, ikEndCtrlGrp, poleVectorCtrlGrp, ikfkBlendCtrlGrp], n = topGrpName)
        mc.parent(ikHandleName, ikEndCtrl)

        mc.setAttr(topGrpName + ".overrideEnabled", 1)
        mc.setAttr(topGrpName + ".overrideRBGColors", 1)
        mc.setAttr(topGrpName + ".overrideColorRBG", self.controllerColor[0], self.controllerColor[1], self.controllerColor[2], type = "double3")
        
class ColorPicker(QWidget):
    colorChanged = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.masterLayout = QVBoxLayout()
        self.color = QColor()
        self.setLayout(self.masterLayout)
        self.pickColorBtn = QPushButton()
        self.pickColorBtn.setStyleSheet(f"background-color:black")
        self.pickColorBtn.clicked.connect(self.PickColorBtnClicked)
        self.masterLayout.addWidget(self.pickColorBtn)

    def PickColorBtnClicked(self):
        self.color = QColorDialog.getColor()
        self.pickColorBtn.setStyleSheet(f"background-color:{self.color.name()}")
        self.colorChanged.emit(self.color)


class LimbRiggerWidget(MayaWindow): # Creates a class called LimbRiggerWidget with parameter MayaWindow
    def __init__(self): # Creates a constructor
        super().__init__() # Calls to inherit from the parent class
        self.rigger = LimbRigger() # Initializes rigger as being equal to class LimbRigger
        self.setWindowTitle("Limb Rigger")
        self.masterLayout = QVBoxLayout() # Initializes masterLayout as being equal to QVBoxLayout
        self.setLayout(self.masterLayout) # Sets layout to masterLayout

        toolTipLabel = QLabel("Select the first joint of the limb, and press the auto find button") # Creates a label that tells the user what to do
        self.masterLayout.addWidget(toolTipLabel) # Puts the label on the UI/Adds toolTipLabel to the Widget

        self.jntsListLineEdit = QLineEdit() # Calls to QLineEdit
        self.masterLayout.addWidget(self.jntsListLineEdit) # Adds jntsListLineEdit to the Widget
        self.jntsListLineEdit.setEnabled(False) # Sets jntsListLineEdit to not be enabled

        autoFindJntBtn = QPushButton("Auto Find") # Creates a button and puts the words Auto Find on it
        autoFindJntBtn.clicked.connect(self.AutoFindJntButtonClicked) # When the button is clicked it calls the function AutoFindJntButtonClicked
        self.masterLayout.addWidget(autoFindJntBtn) # Makes the UI of the button

        ctrlSizeSlider = QSlider()
        ctrlSizeSlider.setOrientation(Qt.Horizontal)
        ctrlSizeSlider.setRange(1, 30)
        ctrlSizeSlider.setValue(self.rigger.controllerSize)
        self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}")
        ctrlSizeSlider.valueChanged.connect(self.CtrlSizeSliderChanged)

        ctrlSizeLayout = QHBoxLayout()
        ctrlSizeLayout.addWidget(ctrlSizeSlider)
        ctrlSizeLayout.addWidget(self.ctrlSizeLabel)
        self.masterLayout.addLayout(ctrlSizeLayout)

        #ctrlColorSlider = mc.floatSlider(min = 0, max = 1, value = 0, step = 0.1, dragCommand = self.ChangeColor)
        #ctrlColorLayout = QHBoxLayout()
        #ctrlColorLayout.addWidget(ctrlColorSlider)
        #self.masterLayout.addLayout(ctrlColorLayout)

        colorPicker = ColorPicker()
        colorPicker.colorChanged.connect(self.ColorPickerChanged)
        self.masterLayout.addWidget(colorPicker)

        setColorBtn = QPushButton("Set Color")
        setColorBtn.clicked.connect(self.SetColorBtnClicked)
        self.masterLayout.addWidget(setColorBtn)

        rigLimbBtn = QPushButton("Rig Limb") # Creates a button with the words Rig Limb on it
        rigLimbBtn.clicked.connect(lambda : self.rigger.RigLimb()) # When pushed the button calls to rigger which then gets the RigLimb function from within the class LimbRigger
        self.masterLayout.addWidget(rigLimbBtn) # Adds button to the Widget/to the UI

    def ColorPickerChanged(self, newColor: QColor):
        self.rigger.controllerColor[0] = newColor.redF()
        self.rigger.controllerColor[1] = newColor.greenF()
        self.rigger.controllerColor[2] = newColor.blueF()

    def SetColorBtnClicked(self):
        curbSelection = mc.ls(sl = True)[0]
        mc.setAttr(curbSelection + ".overrideEnabled", 1)
        mc.setAttr(curbSelection + ".overrideRBGColors", 1)
        mc.setAttr(curbSelection + ".overrideColorRBG", self.rigger.controllerColor[0], self.rigger.controllerColor[1], self.rigger.controllerColor[2], type = "double3")

    #def ChangeColor(self, color):
        #colorValue = int(color*255)
        #grabCurves = mc.ls(s = True, type = "nurbsCurve")
        #mc.setAttr(grabCurves + ".overrideEnabled", 1)
        #mc.setAttr(grabCurves + ".overrideColor", colorValue)

    def CtrlSizeSliderChanged(self,newValue):
        self.ctrlSizeLabel.setText(f"{newValue}")
        self.rigger.controllerSize = newValue

    def AutoFindJntButtonClicked(self): # Defines a function called AutoFindJntButtonClicked with the parameter self
        try: # Tries to do what is below it
            self.rigger.FindJointBasedOnSelection() # Uses rigger to use the function FindJointBasedOnSelection from the LimbRigger class
            self.jntsListLineEdit.setText(f"{self.rigger.root},{self.rigger.mid}, {self.rigger.end}") # Sets the text line in the UI to be set to the name of the joints
        except Exception as e: # Throws an exception when it cannot find the right joints/ when the wrong joints are selected
            QMessageBox.critical(self, "Error", f"{e}") # Gives an error message

limbRiggerWidget = LimbRiggerWidget() # Makes class LimbRiggerWidget equal to a variable
limbRiggerWidget.show() # Displays limbRiggerWidget

GetMayaMainWindow() # calls function GetMayaMainWindow

# ALT + Shift + M to run in Maya
