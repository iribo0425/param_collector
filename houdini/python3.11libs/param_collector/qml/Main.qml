import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import Theme 1.0

Item {
    anchors.fill: parent

    ColumnLayout {
        anchors.fill: parent
        spacing: Theme.spacingM

        MenuBar {
            Layout.fillWidth: true
            Layout.preferredHeight: Theme.controlHeight
            font.pixelSize: Theme.fontSizeM
            delegate: MenuBarItem {
                implicitHeight: Theme.controlHeight
            }

            Menu {
                font.pixelSize: Theme.fontSizeM
                title: "File"
                delegate: MenuItem {
                    implicitHeight: Theme.controlHeight
                }

                Action {
                    shortcut: StandardKey.Open
                    text: "Load Settings..."
                    onTriggered: backend.loadSettings()
                }

                Action {
                    shortcut: StandardKey.Save
                    text: "Save Settings..."
                    onTriggered: backend.saveSettings()
                }
            }
        }
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.leftMargin: Theme.spacingM
            Layout.rightMargin: Theme.spacingM
            spacing: Theme.spacingM

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingM

                Label {
                    Layout.preferredWidth: Theme.rowHeaderWidth
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "Candidate Root Node Path"
                }

                TextField {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: backend.candidateRootNodePath
                    onEditingFinished: backend.candidateRootNodePath = text
                }

                Button {
                    Layout.preferredWidth: Theme.controlHeight
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "..."
                    onClicked: backend.selectCandidateRootNode()
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingM

                Label {
                    Layout.preferredWidth: Theme.rowHeaderWidth
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "Referenced Node Path"
                }

                TextField {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: backend.referencedNodePath
                    onEditingFinished: backend.referencedNodePath = text
                }

                Button {
                    Layout.preferredWidth: Theme.controlHeight
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "..."
                    onClicked: backend.selectReferencedNode()
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingM

                CheckBox {
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "Recursive"
                    checked: backend.recursive
                    onToggled: backend.recursive = checked
                }

                Item {
                    Layout.fillWidth: true
                }
            }

            TabBar {
                id: tabBar
                Layout.fillWidth: true

                TabButton {
                    implicitHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "Copy Create"
                }

                TabButton {
                    implicitHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                    text: "Copy"
                }
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: tabBar.currentIndex

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    NodeList {
                        anchors.fill: parent
                        model: backend.nodeListModel
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ParamTupleReferenceList {
                        anchors.fill: parent
                        model: backend.paramTupleReferenceListModel
                    }
                }
            }
        }

        Button {
            Layout.fillWidth: true
            implicitHeight: Theme.controlHeight
            font.pixelSize: Theme.fontSizeM
            text: "Collect params"
            onClicked: backend.collectParams()
        }
    }
}
