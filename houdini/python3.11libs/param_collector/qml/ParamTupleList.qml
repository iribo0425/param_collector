import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    id: root

    property alias model: listViewParam.model

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
                text: "Params"
                Layout.preferredWidth: Theme.rowHeaderWidth
                Layout.preferredHeight: Theme.controlHeight
                font.pixelSize: Theme.fontSizeM
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignRight
                padding: Theme.spacingXs
            }

            Button {
                text: "+"
                Layout.preferredWidth: Theme.controlHeight
                Layout.preferredHeight: Theme.controlHeight

                onClicked: {
                    if (root.model) {
                        root.model.addRow()
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        ListView {
            id: listViewParam

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: implicitHeight

            clip: true
            spacing: Theme.spacingM
            implicitHeight: contentHeight

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

                        onClicked: {
                            if (root.model) {
                                root.model.removeRowAt(paramItem.index)
                            }
                        }
                    }

                    ComboBox {
                        id: comboBoxParamTextKind

                        Layout.preferredWidth: Theme.rowHeaderWidth
                        Layout.preferredHeight: Theme.controlHeight

                        model: root.model ? root.model.textKindItems : []
                        textRole: "text"
                        valueRole: "value"

                        currentIndex: {
                            const i = comboBoxParamTextKind.indexOfValue(paramItem.textKind)
                            return i >= 0 ? i : (comboBoxParamTextKind.count > 0 ? 0 : -1)
                        }

                        onActivated: function(i) {
                            if (!root.model || i < 0) {
                                return
                            }

                            const value = comboBoxParamTextKind.model[i].value
                            root.model.setTextKindAt(paramItem.index, value)
                        }
                    }

                    TextField {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Theme.controlHeight
                        text: paramItem.text

                        onEditingFinished: {
                            if (root.model) {
                                root.model.setTextAt(paramItem.index, text)
                            }
                        }
                    }
                }
            }
        }
    }
}