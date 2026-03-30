pragma Singleton

import QtQml
import QtQuick

QtObject {
    readonly property int spacingXs: 2
    readonly property int spacingS: 4
    readonly property int spacingM: 6
    readonly property int spacingL: 8
    readonly property int spacingXl: 10

    readonly property int fontSizeXs: 8
    readonly property int fontSizeS: 10
    readonly property int fontSizeM: 12
    readonly property int fontSizeL: 14
    readonly property int fontSizeXl: 16

    readonly property int controlHeight: 25
    readonly property int rowHeaderWidth: 150

    readonly property int listViewBorderWidth: 1
    readonly property color listViewBorderColor: "#CCCCCC"
}
