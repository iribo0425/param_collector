import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    property alias model: listViewParam.model

    Layout.fillWidth: true
    implicitHeight: layoutRoot.implicitHeight + Theme.spacingM * 2

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
                    if (listViewParam.model) {
                        listViewParam.model.addRow()
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        ListView {
            id: listViewParam

            visible: count > 0

            Layout.fillWidth: true
            Layout.topMargin: count > 0 ? Theme.spacingM : 0

            spacing: Theme.spacingM
            clip: true
            interactive: false

            implicitHeight: count > 0 ? contentHeight : 0

            delegate: Rectangle {
                id: paramItem

                required property int index
                required property int textKind
                required property string text

                width: listViewParam.width
                implicitHeight: rowLayout.implicitHeight
                height: implicitHeight

                RowLayout {
                    id: rowLayout
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
                            if (listViewParam.model) {
                                listViewParam.model.removeRowAt(paramItem.index)
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
                                id: comboBoxParamTextKind

                                Layout.preferredWidth: Theme.rowHeaderWidth
                                Layout.preferredHeight: Theme.controlHeight
                                font.pixelSize: Theme.fontSizeM
                                padding: Theme.spacingXs

                                model: listViewParam.model ? listViewParam.model.textKindItems : []
                                textRole: "text"
                                valueRole: "value"

                                currentIndex: {
                                    const i = comboBoxParamTextKind.indexOfValue(paramItem.textKind)
                                    return i >= 0 ? i : (comboBoxParamTextKind.count > 0 ? 0 : -1)
                                }

                                onActivated: {
                                    if (listViewParam.model && paramItem.textKind !== currentValue) {
                                        listViewParam.model.setTextKindAt(
                                            paramItem.index,
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
                                text: paramItem.text

                                onEditingFinished: {
                                    if (listViewParam.model && paramItem.text !== text) {
                                        listViewParam.model.setTextAt(
                                            paramItem.index,
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