import hou
import param_collector.core.common as common
import param_collector.core.copy_create as copy_create
import param_collector.core.create as create
import param_collector.core.settings as sm
import param_collector.model.node_list_model as nlm
import param_collector.model.param_tuple_reference_list_model as ptrlm
import pathlib
import traceback
from PySide6 import QtCore, QtWidgets
import param_collector.lib.jocl.jocl as jocl


def getCurrentNetworkPath() -> str:
    for paneTab in hou.ui.currentPaneTabs():
        if paneTab.type() == hou.paneTabType.NetworkEditor:
            return paneTab.pwd().path()

    return ""


class Backend(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super(Backend, self).__init__(parent)

        self.__candidateRootNodePath: str = ""
        self.__referencedNodePath: str = ""
        self.__recursive: bool = False

        self.__nodeListModel = nlm.NodeListModel(self)
        self.__paramTupleReferenceListModel = ptrlm.ParamTupleReferenceListModel(self)


    candidateRootNodePathChanged: QtCore.Signal = QtCore.Signal(str)


    def getCandidateRootNodePath(self) -> str:
        return self.__candidateRootNodePath


    def setCandidateRootNodePath(self, value: str) -> None:
        if value == self.__candidateRootNodePath:
            return

        self.__candidateRootNodePath = value
        self.candidateRootNodePathChanged.emit(value)


    candidateRootNodePath: QtCore.Property = QtCore.Property(str, getCandidateRootNodePath, setCandidateRootNodePath, notify=candidateRootNodePathChanged)


    referencedNodePathChanged: QtCore.Signal = QtCore.Signal(str)


    def getReferencedNodePath(self) -> str:
        return self.__referencedNodePath


    def setReferencedNodePath(self, value: str) -> None:
        if value == self.__referencedNodePath:
            return

        self.__referencedNodePath = value
        self.referencedNodePathChanged.emit(value)


    referencedNodePath: QtCore.Property = QtCore.Property(str, getReferencedNodePath, setReferencedNodePath, notify=referencedNodePathChanged)


    recursiveChanged: QtCore.Signal = QtCore.Signal(bool)


    def getRecursive(self) -> bool:
        return self.__recursive


    def setRecursive(self, value: bool) -> None:
        if value == self.__recursive:
            return

        self.__recursive = value
        self.recursiveChanged.emit(value)


    recursive: QtCore.Property = QtCore.Property(bool, getRecursive, setRecursive, notify=recursiveChanged)


    def getNodeListModel(self) -> nlm.NodeListModel:
        return self.__nodeListModel


    nodeListModel: QtCore.Property = QtCore.Property(nlm.NodeListModel, getNodeListModel, constant=True)


    def getParamTupleReferenceListModel(self) -> ptrlm.ParamTupleReferenceListModel:
        return self.__paramTupleReferenceListModel


    paramTupleReferenceListModel: QtCore.Property = QtCore.Property(ptrlm.ParamTupleReferenceListModel, getParamTupleReferenceListModel, constant=True)


    @QtCore.Slot()
    def loadSettings(self) -> None:
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent(),
            "Load Settings",
            filter="Settings Files (*.json);;All Files (*)"
        )

        if not filePath:
            return

        ctx: jocl.JsonContext = jocl.JsonContext()
        settings: sm.Settings = jocl.load_convertible(ctx, sm.Settings, pathlib.Path(filePath))

        for issue in ctx.get_issues():
            print(issue)

        self.setCandidateRootNodePath(settings.getCandidateRootNodePath())
        self.setReferencedNodePath(settings.getReferencedNodePath())
        self.setRecursive(settings.getRecursive())

        self.__nodeListModel.setNodes(settings.getNodes())
        self.__paramTupleReferenceListModel.setParamTupleReferences(settings.getParamTupleReferences())


    @QtCore.Slot()
    def saveSettings(self) -> None:
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.parent(),
            "Save Settings",
            filter="Settings Files (*.json);;All Files (*)"
        )

        if not filePath:
            return

        settings: sm.Settings = sm.Settings()
        settings.setCandidateRootNodePath(self.__candidateRootNodePath)
        settings.setReferencedNodePath(self.__referencedNodePath)
        settings.setRecursive(self.__recursive)
        settings.setNodes(self.__nodeListModel.getNodes())
        settings.setParamTupleReferences(self.__paramTupleReferenceListModel.getParamTupleReferences())

        ctx: jocl.JsonContext = jocl.JsonContext()
        jocl.dump_convertible(ctx, settings, pathlib.Path(filePath))

        for issue in ctx.get_issues():
            print(issue)


    @QtCore.Slot()
    def selectCandidateRootNode(self) -> None:
        initialNode: hou.OpNode | None = hou.node(self.getCandidateRootNodePath())

        if initialNode is None:
            currentNetworkPath: str = getCurrentNetworkPath()
            initialNode = hou.node(currentNetworkPath)

        candidateRootNodePath: str = hou.ui.selectNode(initial_node=initialNode)

        if candidateRootNodePath:
            self.setCandidateRootNodePath(candidateRootNodePath)


    @QtCore.Slot()
    def selectReferencedNode(self) -> None:
        initialNode: hou.OpNode | None = hou.node(self.getReferencedNodePath())

        if initialNode is None:
            currentNetworkPath: str = getCurrentNetworkPath()
            initialNode = hou.node(currentNetworkPath)

        referencedNodePath: str = hou.ui.selectNode(initial_node=initialNode)

        if referencedNodePath:
            self.setReferencedNodePath(referencedNodePath)


    def __showMessageDialog(
        self,
        text: str,
        *,
        icon: QtWidgets.QMessageBox.Icon,
        informativeText: str = "",
        detailedText: str = "",
    ) -> None:
        messageDialog = QtWidgets.QMessageBox(hou.qt.mainWindow())
        messageDialog.setWindowTitle("Param Collector")
        messageDialog.setIcon(icon)
        messageDialog.setText(text)

        if informativeText:
            messageDialog.setInformativeText(informativeText)

        if detailedText:
            messageDialog.setDetailedText(detailedText)

        messageDialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        messageDialog.exec()


    def __undoCollectParamsIfNeeded(self) -> None:
        undoLabels: tuple[str, ...] = hou.undos.undoLabels()

        if not undoLabels:
            return

        if undoLabels[0] != "Collect params":
            return

        hou.undos.performUndo()


    @QtCore.Slot()
    def collectParams(self) -> None:
        try:
            with hou.undos.group("Collect params"):
                copy_create.copy_create(
                    self.__candidateRootNodePath,
                    self.__referencedNodePath,
                    self.__nodeListModel.getNodes(),
                    recursive=self.__recursive
                )

                create.create(
                    self.__candidateRootNodePath,
                    self.__referencedNodePath,
                    self.__paramTupleReferenceListModel.getParamTupleReferences(),
                    recursive=self.__recursive
                )

            self.__showMessageDialog(
                "Parameters collected successfully.",
                icon=QtWidgets.QMessageBox.Icon.Information,
            )

        except common.ParamCollectorError as ex:
            self.__undoCollectParamsIfNeeded()

            self.__showMessageDialog(
                "Failed to collect parameters.",
                icon=QtWidgets.QMessageBox.Icon.Critical,
                informativeText=str(ex),
            )

        except Exception:
            self.__undoCollectParamsIfNeeded()

            self.__showMessageDialog(
                "An unexpected error occurred while collecting parameters.",
                icon=QtWidgets.QMessageBox.Icon.Critical,
                informativeText="The changes have been reverted.",
                detailedText=traceback.format_exc(),
            )

