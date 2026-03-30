import param_collector.model.backend as backend
import pathlib
import traceback
from PySide6 import QtCore, QtQml, QtQuick, QtWidgets


def _qtMsgTypeToStr(qtMsgType: QtCore.QtMsgType) -> str:
    d: dict[QtCore.QtMsgType, str] = {
        QtCore.QtMsgType.QtDebugMsg: "Debug",
        QtCore.QtMsgType.QtInfoMsg: "Info",
        QtCore.QtMsgType.QtWarningMsg: "Warning",
        QtCore.QtMsgType.QtCriticalMsg: "Critical",
        QtCore.QtMsgType.QtFatalMsg: "Fatal",
    }
    return d.get(qtMsgType, str(qtMsgType))


_QT_MESSAGE_HANDLER_INSTALLED: bool = False


def _qtMessageHandler(type_: QtCore.QtMsgType, context: QtCore.QMessageLogContext, message: str) -> None:
    filePath: str = getattr(context, "file", "") or ""
    lineNo: int = getattr(context, "line", 0) or 0
    functionName: str = getattr(context, "function", "") or ""
    category: str = getattr(context, "category", "") or ""

    print(
        "[Qt]"
        f"[{_qtMsgTypeToStr(type_)}]"
        f"[{category or '-'}] "
        f"{message} "
        f"({filePath or '-'}:{lineNo} {functionName or '-'})"
    )


def _installQtMessageHandler() -> None:
    global _QT_MESSAGE_HANDLER_INSTALLED

    if _QT_MESSAGE_HANDLER_INSTALLED:
        return

    QtCore.qSetMessagePattern(
        "[%{time yyyy-MM-dd hh:mm:ss.zzz}]"
        "[%{if-category}%{category}%{endif}]"
        "[%{type}] %{message}"
    )

    QtCore.qInstallMessageHandler(_qtMessageHandler)

    _QT_MESSAGE_HANDLER_INSTALLED = True


class MainPanel(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super(MainPanel, self).__init__(parent)

        self.setObjectName("paramCollector")
        self.setWindowTitle("Param Collector")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)

        _installQtMessageHandler()

        self.__backend: backend.Backend = backend.Backend(self)

        self.__quickView: QtQuick.QQuickView = QtQuick.QQuickView()
        self.__quickView.setResizeMode(QtQuick.QQuickView.ResizeMode.SizeRootObjectToView)

        self.__quickView.statusChanged.connect(self.__quickViewOnStatusChanged)
        self.__quickView.sceneGraphError.connect(self.__quickViewOnSceneGraphError)
        self.__quickView.engine().warnings.connect(self.__engineOnWarnings)

        qmlDirPath: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "qml"
        qmlFilePath: pathlib.Path = qmlDirPath / "Main.qml"
        qmlModuleDirPath: pathlib.Path = qmlDirPath / "module"

        self.__quickView.engine().addImportPath(str(qmlDirPath))
        self.__quickView.engine().addImportPath(str(qmlModuleDirPath))

        self.__quickView.rootContext().setContextProperty("backend", self.__backend)

        self.__quickView.setSource(QtCore.QUrl.fromLocalFile(str(qmlFilePath)))

        self.__dumpQmlErrors()

        if self.__quickView.status() == QtQuick.QQuickView.Status.Error:
            raise RuntimeError("Failed to load QML. See log for details.")

        self.__container: QtWidgets.QWidget = QtWidgets.QWidget.createWindowContainer(self.__quickView, self)
        self.__container.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__container)

        self.resize(800, 600)


    def __quickViewOnStatusChanged(self, status: QtQuick.QQuickView.Status) -> None:
        print(f"[QQuickView][Status] {status}")
        self.__dumpQmlErrors()


    def __quickViewOnSceneGraphError(self, error: QtQuick.QQuickWindow.SceneGraphError, message: str) -> None:
        print(f"[QQuickView][SceneGraphError] {message} (error={error})")


    def __engineOnWarnings(self, warnings: list[QtQml.QQmlError]) -> None:
        if not warnings:
            return

        print(f"[QQmlEngine][Warning] Warning Count: {len(warnings)}")

        for warning in warnings:
            print("[QQmlEngine][Warning]", warning.toString())


    def __dumpQmlErrors(self) -> None:
        if self.__quickView.status() != QtQuick.QQuickView.Status.Error:
            return

        errors: list[QtQml.QQmlError] = self.__quickView.errors()

        if not errors:
            print("[QQuickView][Error] Status is Error, but errors() is empty")
            return

        for error in errors:
            print("[QQuickView][Error]", error.toString())


def create() -> QtWidgets.QWidget:
    try:
        panel: MainPanel = MainPanel()
        return panel

    except Exception as e:
        print(f"[MainPanel][InitError] {e}")

        for line in traceback.format_exc().rstrip().splitlines():
            print(f"[MainPanel][Traceback] {line}")

        raise

