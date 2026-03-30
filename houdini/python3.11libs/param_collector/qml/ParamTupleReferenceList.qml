import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0

Rectangle {
    property alias model: listViewReference.model

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
                text: "References"
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
                    if (listViewReference.model) {
                        listViewReference.model.addRow()
                    }
                }
            }

            Item {
                Layout.fillWidth: true
            }
        }

        ListView {
            id: listViewReference

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: implicitHeight

            clip: true
            boundsBehavior: Flickable.StopAtBounds
            spacing: Theme.spacingM

            implicitHeight: contentHeight

            ScrollBar.vertical: ScrollBar {
                id: scrollBarReference
                policy: ScrollBar.AsNeeded
            }

            delegate: Rectangle {
                id: referenceItem

                required property int index
                required property string textKind
                required property string text
                required property var nodeListModel

                width: listViewReference.width - (scrollBarReference.visible ? scrollBarReference.width : 0) - Theme.spacingS
                implicitHeight: referenceItemLayout.implicitHeight
                height: implicitHeight

                RowLayout {
                    id: referenceItemLayout
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
                            if (listViewReference.model) {
                                listViewReference.model.removeRowAt(referenceItem.index)
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
                                id: comboBoxReferenceTextKind

                                Layout.preferredWidth: Theme.rowHeaderWidth
                                Layout.preferredHeight: Theme.controlHeight
                                font.pixelSize: Theme.fontSizeM
                                padding: Theme.spacingXs

                                model: [
                                    { label: "Name", value: "NAME" },
                                    { label: "Label", value: "LABEL" }
                                ]
                                textRole: "label"
                                valueRole: "value"

                                currentIndex: {
                                    const i = comboBoxReferenceTextKind.indexOfValue(referenceItem.textKind)
                                    return i >= 0 ? i : (comboBoxReferenceTextKind.count > 0 ? 0 : -1)
                                }

                                onActivated: {
                                    if (listViewReference.model && referenceItem.textKind !== currentValue) {
                                        listViewReference.model.setTextKindAt(
                                            referenceItem.index,
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
                                text: referenceItem.text

                                onEditingFinished: {
                                    if (listViewReference.model && referenceItem.text !== text) {
                                        listViewReference.model.setTextAt(
                                            referenceItem.index,
                                            text
                                        )
                                    }
                                }
                            }
                        }

                        NodeList {
                            Layout.fillWidth: true
                            model: referenceItem.nodeListModel
                        }
                    }
                }
            }
        }
    }
}