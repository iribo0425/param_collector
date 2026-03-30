import copy
import enum
import param_collector.core.common as common
import param_collector.core.create as create
import param_collector.model.node_list_model as nlm
from PySide6 import QtCore


class ParamTupleReferenceListModelRole(enum.IntEnum):
    TEXT_KIND = QtCore.Qt.UserRole + 1
    TEXT = QtCore.Qt.UserRole + 2
    NODE_LIST_MODEL = QtCore.Qt.UserRole + 3


class ParamTupleReferenceListModel(QtCore.QAbstractListModel):
    def __init__(self, parent: QtCore.QObject | None = None):
        super(ParamTupleReferenceListModel, self).__init__(parent)

        self.__paramTupleReferences: list[create.ParamTupleReference] = []
        self.__nodeListModels: list[nlm.NodeListModel] = []


    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> object:
        if not self.__isValidIndex(index):
            return None

        paramTupleReference: create.ParamTupleReference = self.__paramTupleReferences[index.row()]

        if role == ParamTupleReferenceListModelRole.TEXT_KIND:
            return paramTupleReference.getReferencedParamTuple().getTextKind().value

        if role == ParamTupleReferenceListModelRole.TEXT:
            return paramTupleReference.getReferencedParamTuple().getText()

        if role == ParamTupleReferenceListModelRole.NODE_LIST_MODEL:
            return self.__nodeListModels[index.row()]

        return None


    def setData(self, index: QtCore.QModelIndex, value: object, role: int = QtCore.Qt.EditRole) -> bool:
        if not self.__isValidIndex(index):
            return False

        paramTupleReference: create.ParamTupleReference = self.__paramTupleReferences[index.row()]

        if role == ParamTupleReferenceListModelRole.TEXT_KIND:
            textKind: common.ParamTupleTextKind | None = common.ParamTupleTextKind.tryGetFromValue(value)

            if (textKind is None) or (paramTupleReference.getReferencedParamTuple().getTextKind() == textKind):
                return False

            paramTupleReference.getReferencedParamTuple().setTextKind(textKind)
            self.dataChanged.emit(index, index, [role])
            return True

        if role == ParamTupleReferenceListModelRole.TEXT:
            if (not isinstance(value, str)) or (paramTupleReference.getReferencedParamTuple().getText() == value):
                return False

            paramTupleReference.getReferencedParamTuple().setText(value)
            self.dataChanged.emit(index, index, [role])
            return True

        return False


    def roleNames(self) -> dict[int, bytes]:
        return {
            ParamTupleReferenceListModelRole.TEXT_KIND: b"textKind",
            ParamTupleReferenceListModelRole.TEXT: b"text",
            ParamTupleReferenceListModelRole.NODE_LIST_MODEL: b"nodeListModel",
        }


    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0

        return len(self.__paramTupleReferences)


    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not self.__isValidIndex(index):
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    @QtCore.Slot()
    def addRow(self) -> None:
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__paramTupleReferences), len(self.__paramTupleReferences))

        paramTupleReference: create.ParamTupleReference = create.ParamTupleReference()
        self.__paramTupleReferences.append(paramTupleReference)

        nodeListModel: nlm.NodeListModel = nlm.NodeListModel(self)
        nodeListModel.bindNodes(paramTupleReference.getReferringNodes())
        self.__nodeListModels.append(nodeListModel)

        self.endInsertRows()


    @QtCore.Slot(int)
    def removeRowAt(self, rowIndex: int) -> None:
        if not self.__isValidRowIndex(rowIndex):
            return

        self.beginRemoveRows(QtCore.QModelIndex(), rowIndex, rowIndex)

        self.__paramTupleReferences.pop(rowIndex)
        nodeListModel: nlm.NodeListModel = self.__nodeListModels.pop(rowIndex)
        nodeListModel.deleteLater()

        self.endRemoveRows()


    @QtCore.Slot(int, int, result=bool)
    def setTextKindAt(self, rowIndex: int, value: int) -> bool:
        return self.setData(self.index(rowIndex, 0), value, ParamTupleReferenceListModelRole.TEXT_KIND)


    @QtCore.Slot(int, str, result=bool)
    def setTextAt(self, rowIndex: int, value: str) -> bool:
        return self.setData(self.index(rowIndex, 0), value, ParamTupleReferenceListModelRole.TEXT)


    def getParamTupleReferences(self) -> list[create.ParamTupleReference]:
        return copy.deepcopy(self.__paramTupleReferences)


    def setParamTupleReferences(self, value: list[create.ParamTupleReference]) -> None:
        oldNodeListModels: list[nlm.NodeListModel] = self.__nodeListModels

        self.beginResetModel()

        self.__paramTupleReferences = copy.deepcopy(value)
        self.__nodeListModels = []

        for paramTupleReference in self.__paramTupleReferences:
            nodeListModel: nlm.NodeListModel = nlm.NodeListModel(self)
            nodeListModel.bindNodes(paramTupleReference.getReferringNodes())
            self.__nodeListModels.append(nodeListModel)

        self.endResetModel()

        for oldNodeListModel in oldNodeListModels:
            oldNodeListModel.deleteLater()


    def bindParamTupleReferences(self, paramTupleReferences: list[create.ParamTupleReference]) -> None:
        oldNodeListModels: list[nlm.NodeListModel] = self.__nodeListModels

        self.beginResetModel()

        self.__paramTupleReferences = paramTupleReferences
        self.__nodeListModels = []

        for paramTupleReference in self.__paramTupleReferences:
            nodeListModel: nlm.NodeListModel = nlm.NodeListModel(self)
            nodeListModel.bindNodes(paramTupleReference.getReferringNodes())
            self.__nodeListModels.append(nodeListModel)

        self.endResetModel()

        for oldNodeListModel in oldNodeListModels:
            oldNodeListModel.deleteLater()


    def __isValidRowIndex(self, rowIndex: int) -> bool:
        return 0 <= rowIndex < len(self.__paramTupleReferences)


    def __isValidIndex(self, index: QtCore.QModelIndex) -> bool:
        return index.isValid() and (index.column() == 0) and self.__isValidRowIndex(index.row())

