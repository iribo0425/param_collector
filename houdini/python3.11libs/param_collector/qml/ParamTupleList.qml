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
                text: "Params"
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

            visible: count > 0

            Layout.fillWidth: true
            Layout.topMargin: count > 0 ? Theme.spacingM : 0

            spacing: Theme.spacingM
            clip: true
            interactive: false

            implicitHeight: count > 0 ? contentHeight : 0

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
                        text: "×"
                        Layout.preferredWidth: Theme.controlHeight
                        Layout.preferredHeight: Theme.controlHeight
                        Layout.alignment: Qt.AlignTop
                        font.pixelSize: Theme.fontSizeM
                        padding: Theme.spacingXs

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
                                padding: Theme.spacingXs

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