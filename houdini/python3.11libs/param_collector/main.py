import logging
import param_collector.core.system as system
import param_collector.panel.main_panel as main_panel

from PySide6 import QtWidgets
from param_collector.core.system import ToolMode


logger: logging.Logger = logging.getLogger(__name__)


def createMainPanel(toolMode: ToolMode) -> QtWidgets.QWidget:
    try:
        system.configureLogging(toolMode)

        panel: main_panel.MainPanel = main_panel.MainPanel()

        return panel

    except Exception:
        logger.exception("Failed to initialize Param Collector")

        QtWidgets.QMessageBox.critical(
            None,
            "Param Collector",
            "Failed to initialize Param Collector.\n\nSee log for details.",
        )

        raise

