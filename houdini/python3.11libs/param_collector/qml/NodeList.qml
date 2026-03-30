import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    property alias model: listViewNode.model
    property bool contentDrivenHeight: false

    Layout.fillWidth: true
    Layout.fillHeight: !contentDrivenHeight

    implicitHeight: {
        if (!contentDrivenHeight) {
            return 0
        }

        const margins = Theme.spacingM * 2
        const headerHeight = Theme.controlHeight
        const listTopMargin = listViewNode.count > 0 ? Theme.spacingM : 0
        const listHeight = listViewNode.count > 0 ? listViewNode.contentHeight : 0

        return margins + headerHeight + listTopMargin + listHeight
    }

    border.width: Theme.listViewBorderWidth
    border.color: Theme.listViewBorderColor

    ColumnLayout {
        id: layoutRoot
        anchors.fill: parent
        anchors.margins: Theme.spacingM
        spacing: 0

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

            visible: !contentDrivenHeight || count > 0

            Layout.fillWidth: true
            Layout.fillHeight: !contentDrivenHeight
            Layout.topMargin: count > 0 ? Theme.spacingM : 0

            clip: true
            boundsBehavior: Flickable.StopAtBounds
            spacing: Theme.spacingM
            interactive: !contentDrivenHeight

            implicitHeight: contentDrivenHeight && count > 0 ? contentHeight : 0

            ScrollBar.vertical: ScrollBar {
                id: scrollBarNode
                policy: contentDrivenHeight ? ScrollBar.AlwaysOff : ScrollBar.AsNeeded
            }

            delegate: Rectangle {
                required property int index
                required property int textKind
                required property string text
                required property var paramTupleListModel

                id: nodeItem
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
                                model: listViewNode.model ? listViewNode.model.textKindItems : []
                                textRole: "text"
                                valueRole: "value"

                                currentIndex: {
                                    const i = comboBoxNodeTextKind.indexOfValue(nodeItem.textKind)
                                    return i >= 0 ? i : (comboBoxNodeTextKind.count > 0 ? 0 : -1)
                                }

                                onActivated: {
                                    if (listViewNode.model && nodeItem.textKind !== currentValue) {
                                        listViewNode.model.setTextKindAt(nodeItem.index, currentValue)
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
                                        listViewNode.model.setTextAt(nodeItem.index, text)
                                    }
                                }
                            }
                        }

                        ParamTupleList {
                            Layout.fillWidth: true
                            model: nodeItem.paramTupleListModel
                        }
                    }
                }
            }
        }
    }
}