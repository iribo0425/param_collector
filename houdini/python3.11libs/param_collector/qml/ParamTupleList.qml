import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    property alias model: listView.model
    Layout.fillWidth: true
    implicitHeight: rootLayout.implicitHeight + Theme.spacingM * 2
    border.width: Theme.listViewBorderWidth
    border.color: Theme.listViewBorderColor

    ColumnLayout {
        id: rootLayout
        anchors.fill: parent
        anchors.margins: Theme.spacingM
        spacing: 0

        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingM

            Label {
                Layout.preferredHeight: Theme.controlHeight
                font.pixelSize: Theme.fontSizeM
                verticalAlignment: Text.AlignVCenter
                text: "Params"
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
            Layout.topMargin: count > 0 ? Theme.spacingM : 0
            implicitHeight: count > 0 ? contentHeight : 0
            visible: count > 0
            clip: true
            spacing: Theme.spacingM
            interactive: false

            delegate: Rectangle {
                id: listViewItem
                required property int index
                required property int textKind
                required property string text
                width: listView.width
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
                                model: listView.model ? listView.model.textKindItems : []
                                textRole: "text"
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
                    }
                }
            }
        }
    }
}
