import copy
import enum
import param_collector.core.common as common
import param_collector.model.param_tuple_list_model as ptlm
from PySide6 import QtCore


class NodeListModelRole(enum.IntEnum):
    TEXT_KIND = QtCore.Qt.UserRole + 1
    TEXT = QtCore.Qt.UserRole + 2
    PARAM_TUPLE_LIST_MODEL = QtCore.Qt.UserRole + 3


class NodeListModel(QtCore.QAbstractListModel):
    __TEXT_KIND_ITEMS: list[dict[str, str | int]] = [
        {"text": m.name.title(), "value": int(m)}
        for m in common.NodeTextKind
    ]


    def __init__(self, parent: QtCore.QObject | None = None):
        super(NodeListModel, self).__init__(parent)

        self.__nodes: list[common.Node] = []
        self.__paramTupleListModels: list[ptlm.ParamTupleListModel] = []


    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> object:
        if not self.__isValidIndex(index):
            return None

        node: common.Node = self.__nodes[index.row()]

        if role == NodeListModelRole.TEXT_KIND:
            return node.getTextKind().value

        if role == NodeListModelRole.TEXT:
            return node.getText()

        if role == NodeListModelRole.PARAM_TUPLE_LIST_MODEL:
            return self.__paramTupleListModels[index.row()]

        return None


    def setData(self, index: QtCore.QModelIndex, value: object, role: int = QtCore.Qt.EditRole) -> bool:
        if not self.__isValidIndex(index):
            return False

        node: common.Node = self.__nodes[index.row()]

        if role == NodeListModelRole.TEXT_KIND:
            textKind: common.NodeTextKind | None = common.NodeTextKind.tryGetFromValue(value)

            if (textKind is None) or (node.getTextKind() == textKind):
                return False

            node.setTextKind(textKind)
            self.dataChanged.emit(index, index, [role])
            return True

        if role == NodeListModelRole.TEXT:
            if (not isinstance(value, str)) or (node.getText() == value):
                return False

            node.setText(value)
            self.dataChanged.emit(index, index, [role])
            return True

        return False


    def roleNames(self) -> dict[int, bytes]:
        return {
            NodeListModelRole.TEXT_KIND: b"textKind",
            NodeListModelRole.TEXT: b"text",
            NodeListModelRole.PARAM_TUPLE_LIST_MODEL: b"paramTupleListModel",
        }


    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0

        return len(self.__nodes)


    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not self.__isValidIndex(index):
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    @QtCore.Slot()
    def addRow(self) -> None:
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__nodes), len(self.__nodes))

        node: common.Node = common.Node()
        self.__nodes.append(node)

        paramTupleListModel: ptlm.ParamTupleListModel = ptlm.ParamTupleListModel(self)
        paramTupleListModel.bindParamTuples(node.getParamTuples())
        self.__paramTupleListModels.append(paramTupleListModel)

        self.endInsertRows()


    @QtCore.Slot(int)
    def removeRowAt(self, rowIndex: int) -> None:
        if not self.__isValidRowIndex(rowIndex):
            return

        self.beginRemoveRows(QtCore.QModelIndex(), rowIndex, rowIndex)

        self.__nodes.pop(rowIndex)
        paramTupleModel: ptlm.ParamTupleListModel = self.__paramTupleListModels.pop(rowIndex)
        paramTupleModel.deleteLater()

        self.endRemoveRows()


    @QtCore.Property("QVariantList", constant=True)
    def textKindItems(self) -> list[dict[str, str | int]]:
        return NodeListModel.__TEXT_KIND_ITEMS


    @QtCore.Slot(int, int, result=bool)
    def setTextKindAt(self, rowIndex: int, value: int) -> bool:
        return self.setData(self.index(rowIndex, 0), value, NodeListModelRole.TEXT_KIND)


    @QtCore.Slot(int, str, result=bool)
    def setTextAt(self, rowIndex: int, value: str) -> bool:
        return self.setData(self.index(rowIndex, 0), value, NodeListModelRole.TEXT)


    def getNodes(self) -> list[common.Node]:
        return copy.deepcopy(self.__nodes)


    def setNodes(self, value: list[common.Node]) -> None:
        oldParamTupleListModels = self.__paramTupleListModels

        self.beginResetModel()

        self.__nodes = copy.deepcopy(value)
        self.__paramTupleListModels = []

        for node in self.__nodes:
            paramTupleListModel = ptlm.ParamTupleListModel(self)
            paramTupleListModel.bindParamTuples(node.getParamTuples())
            self.__paramTupleListModels.append(paramTupleListModel)

        self.endResetModel()

        for oldModel in oldParamTupleListModels:
            oldModel.deleteLater()


    def bindNodes(self, nodes: list[common.Node]) -> None:
        oldParamTupleListModels = self.__paramTupleListModels

        self.beginResetModel()

        self.__nodes = nodes
        self.__paramTupleListModels = []

        for node in self.__nodes:
            paramTupleListModel = ptlm.ParamTupleListModel(self)
            paramTupleListModel.bindParamTuples(node.getParamTuples())
            self.__paramTupleListModels.append(paramTupleListModel)

        self.endResetModel()

        for oldModel in oldParamTupleListModels:
            oldModel.deleteLater()


    def __isValidRowIndex(self, rowIndex: int) -> bool:
        return 0 <= rowIndex < len(self.__nodes)


    def __isValidIndex(self, index: QtCore.QModelIndex) -> bool:
        return index.isValid() and (index.column() == 0) and self.__isValidRowIndex(index.row())

