import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    property alias model: listViewNode.model

    Layout.fillWidth: true
    Layout.fillHeight: true

    implicitHeight: layoutRoot.implicitHeight
    border.width: Theme.listViewBorderWidth
    border.color: Theme.listViewBorderColor

    ColumnLayout {
        id: layoutRoot
        anchors.fill: parent
        spacing: Theme.spacingM

        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingM

            Label {
                text: "Nodes"
                Layout.preferredHeight: Theme.controlHeight
                font.pixelSize: Theme.fontSizeM
                verticalAlignment: Text.AlignVCenter
            }

            Button {
                text: "+"
                Layout.preferredWidth: Theme.controlHeight
                Layout.preferredHeight: Theme.controlHeight
                font.pixelSize: Theme.fontSizeM
                padding: Theme.spacingXs

                onClicked: {
                    if (listViewNode.model) {
                        listViewNode.model.addRow()
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        ListView {
            id: listViewNode

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: implicitHeight

            clip: true
            boundsBehavior: Flickable.StopAtBounds
            spacing: Theme.spacingM

            implicitHeight: contentHeight

            ScrollBar.vertical: ScrollBar {
                id: scrollBarNode
                policy: ScrollBar.AsNeeded
            }

            delegate: Rectangle {
                id: nodeItem

                required property int index
                required property int textKind
                required property string text
                required property var paramTupleListModel

                width: listViewNode.width - (scrollBarNode.visible ? scrollBarNode.width : 0) - Theme.spacingS
                implicitHeight: nodeItemLayout.implicitHeight
                height: implicitHeight

                RowLayout {
                    id: nodeItemLayout
                    width: parent.width
                    spacing: Theme.spacingM

                    Button {
                        text: "×"
                        Layout.preferredWidth: Theme.controlHeight
                        Layout.preferredHeight: Theme.controlHeight
                        Layout.alignment: Qt.AlignTop
                        font.pixelSize: Theme.fontSizeM
                        padding: Theme.spacingXs

                        onClicked: {
                            if (listViewNode.model) {
                                listViewNode.model.removeRowAt(nodeItem.index)
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: Theme.spacingM

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: Theme.spacingM

                            ComboBox {
                                id: comboBoxNodeTextKind

                                Layout.preferredWidth: Theme.rowHeaderWidth
                                Layout.preferredHeight: Theme.controlHeight
                                font.pixelSize: Theme.fontSizeM
                                padding: Theme.spacingXs

                                model: listViewNode.model.textKindItems
                                textRole: "text"
                                valueRole: "value"

                                currentIndex: {
                                    const i = comboBoxNodeTextKind.indexOfValue(nodeItem.textKind)
                                    return i >= 0 ? i : (comboBoxNodeTextKind.count > 0 ? 0 : -1)
                                }

                                onActivated: {
                                    if (listViewNode.model && nodeItem.textKind !== currentValue) {
                                        listViewNode.model.setTextKindAt(
                                            nodeItem.index,
                                            currentValue
                                        )
                                    }
                                }

                                indicator: Text {
                                    text: "▼"
                                    font.pixelSize: Theme.fontSizeXs
                                    anchors.right: parent.right
                                    anchors.rightMargin: Theme.spacingM
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }

                            TextField {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Theme.controlHeight
                                font.pixelSize: Theme.fontSizeM
                                padding: Theme.spacingXs
                                text: nodeItem.text

                                onEditingFinished: {
                                    if (listViewNode.model && nodeItem.text !== text) {
                                        listViewNode.model.setTextAt(
                                            nodeItem.index,
                                            text
                                        )
                                    }
                                }
                            }
                        }

                        ParamTupleList {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: nodeItem.paramTupleListModel
                        }
                    }
                }
            }
        }
    }
}