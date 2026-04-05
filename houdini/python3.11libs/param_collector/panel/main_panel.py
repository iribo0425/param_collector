import logging
import param_collector.model.backend as backend
import pathlib
from PySide6 import QtCore, QtQml, QtQuick, QtWidgets


logger: logging.Logger = logging.getLogger(__name__)


class MainPanel(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super(MainPanel, self).__init__(parent)

        self.setObjectName("paramCollector")
        self.setWindowTitle("Param Collector")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.__backend: backend.Backend = backend.Backend(self)
        self.__quickView: QtQuick.QQuickView | None = None
        self.__windowContainer: QtWidgets.QWidget | None = None

        try:
            self.__quickView = QtQuick.QQuickView()
            self.__quickView.setResizeMode(QtQuick.QQuickView.ResizeMode.SizeRootObjectToView)
            self.__quickView.statusChanged.connect(self.__quickView_statusChanged)
            self.__quickView.sceneGraphError.connect(self.__quickView_sceneGraphError)

            engine: QtQml.QQmlEngine = self.__quickView.engine()

            if hasattr(engine, "setOutputWarningsToStandardError"):
                engine.setOutputWarningsToStandardError(False)

            engine.warnings.connect(self.__engine_warnings)

            qmlDirPath: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "qml"
            qmlFilePath: pathlib.Path = qmlDirPath / "Main.qml"
            qmlModuleDirPath: pathlib.Path = qmlDirPath / "module"

            engine.addImportPath(str(qmlDirPath))
            engine.addImportPath(str(qmlModuleDirPath))
            self.__quickView.rootContext().setContextProperty("backend", self.__backend)

            self.__quickView.setSource(QtCore.QUrl.fromLocalFile(str(qmlFilePath)))
            self.__dumpErrors()

            if self.__quickView.status() == QtQuick.QQuickView.Status.Error:
                raise RuntimeError("Failed to load QML. See log for details.")

            self.__windowContainer = QtWidgets.QWidget.createWindowContainer(self.__quickView, self)
            self.__windowContainer.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

            layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(self.__windowContainer)

            self.resize(800, 600)

        except Exception:
            self.__cleanupQuickObjects()
            raise


    def closeEvent(self, event) -> None:
        self.__cleanupQuickObjects()
        super().closeEvent(event)


    def __cleanupQuickObjects(self) -> None:
        if self.__windowContainer is not None:
            self.__windowContainer.close()
            self.__windowContainer.deleteLater()
            self.__windowContainer = None
            self.__quickView = None
            return

        if self.__quickView is not None:
            self.__quickView.close()
            self.__quickView.deleteLater()
            self.__quickView = None


    def __quickView_statusChanged(self, status: QtQuick.QQuickView.Status) -> None:
        logger.debug("QQuickView status changed: %s", status)
        self.__dumpErrors()


    def __quickView_sceneGraphError(self, error: QtQuick.QQuickWindow.SceneGraphError, message: str) -> None:
        errorNameMap: dict[QtQuick.QQuickWindow.SceneGraphError, str] = {
            QtQuick.QQuickWindow.SceneGraphError.ContextNotAvailable: "ContextNotAvailable",
        }
        errorName: str = errorNameMap.get(error, str(error))
        fullMessage: str = (
            "A Qt Quick scene graph error occurred.\n\n"
            f"Error: {errorName}\n"
            f"Message: {message}"
        )

        logger.critical(
            "QQuickView scene graph error. error=%s message=%s",
            errorName,
            message,
        )

        QtWidgets.QMessageBox.critical(
            self,
            "Param Collector",
            fullMessage,
        )

        self.setEnabled(False)
        self.close()


    def __engine_warnings(self, warnings: list[QtQml.QQmlError]) -> None:
        if not warnings:
            return

        logger.warning("QQmlEngine emitted %d warning(s)", len(warnings))

        for warning in warnings:
            logger.warning("QML warning: %s", warning.toString())


    def __dumpErrors(self) -> None:
        if self.__quickView is None:
            return

        if self.__quickView.status() != QtQuick.QQuickView.Status.Error:
            return

        errors: list[QtQml.QQmlError] = self.__quickView.errors()

        if not errors:
            logger.error("QQuickView status is Error, but errors() is empty")
            return

        for error in errors:
            logger.error("QML error: %s", error.toString())

