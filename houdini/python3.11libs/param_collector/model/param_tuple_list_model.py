import copy
import enum
import param_collector.core.common as common
from PySide6 import QtCore


class ParamTupleListModelRole(enum.IntEnum):
    TEXT_KIND = QtCore.Qt.UserRole + 1
    TEXT = QtCore.Qt.UserRole + 2


class ParamTupleListModel(QtCore.QAbstractListModel):
    __TEXT_KIND_ITEMS: list[dict[str, str | int]] = [
        {"text": m.name.title(), "value": int(m)}
        for m in common.ParamTupleTextKind
    ]


    def __init__(self, parent: QtCore.QObject | None = None):
        super(ParamTupleListModel, self).__init__(parent)

        self.__paramTuples: list[common.ParamTuple] = []


    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> object:
        if not self.__isValidIndex(index):
            return None

        paramTuple: common.ParamTuple = self.__paramTuples[index.row()]

        if role == ParamTupleListModelRole.TEXT_KIND:
            return paramTuple.getTextKind().value

        if role == ParamTupleListModelRole.TEXT:
            return paramTuple.getText()

        return None


    def setData(self, index: QtCore.QModelIndex, value: object, role: int = QtCore.Qt.EditRole) -> bool:
        if not self.__isValidIndex(index):
            return False

        paramTuple: common.ParamTuple = self.__paramTuples[index.row()]

        if role == ParamTupleListModelRole.TEXT_KIND:
            textKind: common.ParamTupleTextKind | None = common.ParamTupleTextKind.tryGetFromValue(value)

            if (textKind is None) or (paramTuple.getTextKind() == textKind):
                return False

            paramTuple.setTextKind(textKind)
            self.dataChanged.emit(index, index, [role])
            return True

        if role == ParamTupleListModelRole.TEXT:
            if (not isinstance(value, str)) or (paramTuple.getText() == value):
                return False

            paramTuple.setText(value)
            self.dataChanged.emit(index, index, [role])
            return True

        return False


    def roleNames(self) -> dict[int, bytes]:
        return {
            ParamTupleListModelRole.TEXT_KIND: b"textKind",
            ParamTupleListModelRole.TEXT: b"text",
        }


    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0

        return len(self.__paramTuples)


    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not self.__isValidIndex(index):
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    @QtCore.Property("QVariantList", constant=True)
    def textKindItems(self) -> list[dict[str, str | int]]:
        return ParamTupleListModel.__TEXT_KIND_ITEMS


    @QtCore.Slot()
    def addRow(self) -> None:
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__paramTuples), len(self.__paramTuples))
        self.__paramTuples.append(common.ParamTuple())
        self.endInsertRows()


    @QtCore.Slot(int)
    def removeRowAt(self, rowIndex: int) -> None:
        if not self.__isValidRowIndex(rowIndex):
            return

        self.beginRemoveRows(QtCore.QModelIndex(), rowIndex, rowIndex)
        self.__paramTuples.pop(rowIndex)
        self.endRemoveRows()


    @QtCore.Slot(int, int, result=bool)
    def setTextKindAt(self, rowIndex: int, value: int) -> bool:
        return self.setData(self.index(rowIndex, 0), value, ParamTupleListModelRole.TEXT_KIND)


    @QtCore.Slot(int, str, result=bool)
    def setTextAt(self, rowIndex: int, value: str) -> bool:
        return self.setData(self.index(rowIndex, 0), value, ParamTupleListModelRole.TEXT)


    def getParamTuples(self) -> list[common.ParamTuple]:
        return copy.deepcopy(self.__paramTuples)


    def setParamTuples(self, value: list[common.ParamTuple]) -> None:
        self.beginResetModel()
        self.__paramTuples = copy.deepcopy(value)
        self.endResetModel()


    def bindParamTuples(self, paramTuples: list[common.ParamTuple]) -> None:
        self.beginResetModel()
        self.__paramTuples = paramTuples
        self.endResetModel()


    def __isValidRowIndex(self, rowIndex: int) -> bool:
        return 0 <= rowIndex < len(self.__paramTuples)


    def __isValidIndex(self, index: QtCore.QModelIndex) -> bool:
        return index.isValid() and (index.column() == 0) and self.__isValidRowIndex(index.row())

