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
                title: "File"
                font.pixelSize: Theme.fontSizeM
                topPadding: 2
                bottomPadding: 2

                delegate: MenuItem {
                    implicitHeight: Theme.controlHeight
                }

                Action {
                    onTriggered: backend.loadSettings()
                    shortcut: StandardKey.Open
                    text: "Load Settings..."
                }

                Action {
                    onTriggered: backend.saveSettings()
                    shortcut: StandardKey.Save
                    text: "Save Settings..."
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
                    text: "Candidate Root Node Path"
                    Layout.preferredWidth: Theme.rowHeaderWidth
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }

                TextField {
                    text: backend.candidateRootNodePath
                    onEditingFinished: backend.candidateRootNodePath = text
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }

                Button {
                    text: "..."
                    onClicked: backend.selectCandidateRootNode()
                    Layout.preferredWidth: Theme.controlHeight
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingM

                Label {
                    text: "Referenced Node Path"
                    Layout.preferredWidth: Theme.rowHeaderWidth
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }

                TextField {
                    text: backend.referencedNodePath
                    onEditingFinished: backend.referencedNodePath = text
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }

                Button {
                    text: "..."
                    onClicked: backend.selectReferencedNode()
                    Layout.preferredWidth: Theme.controlHeight
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingM

                CheckBox {
                    text: "Recursive"
                    checked: backend.recursive
                    onToggled: backend.recursive = checked
                    Layout.preferredHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }

                Item {
                    Layout.fillWidth: true
                }
            }

            TabBar {
                id: tabBar
                Layout.fillWidth: true

                TabButton {
                    text: "Copy Create"
                    implicitHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }

                TabButton {
                    text: "Copy"
                    implicitHeight: Theme.controlHeight
                    font.pixelSize: Theme.fontSizeM
                }
            }

            StackLayout {
                currentIndex: tabBar.currentIndex
                Layout.fillWidth: true
                Layout.fillHeight: true

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
            text: "Collect params"
            onClicked: backend.collectParams()
            Layout.fillWidth: true
            implicitHeight: Theme.controlHeight
            font.pixelSize: Theme.fontSizeM
        }
    }
}