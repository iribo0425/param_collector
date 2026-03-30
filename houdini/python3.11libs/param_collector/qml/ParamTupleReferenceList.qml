import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    property alias model: listView.model
    Layout.fillWidth: true
    Layout.fillHeight: true
    implicitHeight: rootLayout.implicitHeight
    border.width: Theme.listViewBorderWidth
    border.color: Theme.listViewBorderColor

    ColumnLayout {
        id: rootLayout
        anchors.fill: parent
        anchors.margins: Theme.spacingM
        spacing: Theme.spacingM

        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingM

            Label {
                Layout.preferredHeight: Theme.controlHeight
                font.pixelSize: Theme.fontSizeM
                verticalAlignment: Text.AlignVCenter
                text: "References"
            }

            Button {
                Layout.preferredWidth: Theme.controlHeight
                Layout.preferredHeight: Theme.controlHeight
                font.pixelSize: Theme.fontSizeM
                text: "+"
                onClicked: {
                    if (listView.model) {
                        listView.model.addRow()
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        ListView {
            id: listView
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: implicitHeight
            implicitHeight: contentHeight
            clip: true
            boundsBehavior: Flickable.StopAtBounds
            spacing: Theme.spacingM

            ScrollBar.vertical: ScrollBar {
                id: scrollBar
                policy: ScrollBar.AsNeeded
            }

            delegate: Rectangle {
                id: listViewItem
                required property int index
                required property string textKind
                required property string text
                required property var nodeListModel
                width: listView.width - (scrollBar.visible ? scrollBar.width : 0) - Theme.spacingS
                implicitHeight: listViewItemLayout.implicitHeight
                height: implicitHeight

                RowLayout {
                    id: listViewItemLayout
                    width: parent.width
                    spacing: Theme.spacingM

                    Button {
                        Layout.preferredWidth: Theme.controlHeight
                        Layout.preferredHeight: Theme.controlHeight
                        Layout.alignment: Qt.AlignTop
                        font.pixelSize: Theme.fontSizeM
                        text: "×"
                        onClicked: {
                            if (listView.model) {
                                listView.model.removeRowAt(listViewItem.index)
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
                                id: textKindComboBox
                                Layout.preferredWidth: Theme.rowHeaderWidth
                                Layout.preferredHeight: Theme.controlHeight
                                font.pixelSize: Theme.fontSizeM
                                model: [
                                    { label: "Name", value: "NAME" },
                                    { label: "Label", value: "LABEL" }
                                ]
                                textRole: "label"
                                valueRole: "value"
                                currentIndex: {
                                    const i = textKindComboBox.indexOfValue(listViewItem.textKind)
                                    return i >= 0 ? i : (textKindComboBox.count > 0 ? 0 : -1)
                                }
                                onActivated: {
                                    if (listView.model && listViewItem.textKind !== currentValue) {
                                        listView.model.setTextKindAt(
                                            listViewItem.index,
                                            currentValue
                                        )
                                    }
                                }
                                indicator: Text {
                                    anchors.right: parent.right
                                    anchors.rightMargin: Theme.spacingM
                                    anchors.verticalCenter: parent.verticalCenter
                                    font.pixelSize: Theme.fontSizeXs
                                    text: "▼"
                                }
                            }

                            TextField {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Theme.controlHeight
                                font.pixelSize: Theme.fontSizeM
                                text: listViewItem.text
                                onEditingFinished: {
                                    if (listView.model && listViewItem.text !== text) {
                                        listView.model.setTextAt(
                                            listViewItem.index,
                                            text
                                        )
                                    }
                                }
                            }
                        }

                        NodeList {
                            Layout.fillWidth: true
                            contentDrivenHeight: true
                            model: listViewItem.nodeListModel
                        }
                    }
                }
            }
        }
    }
}
