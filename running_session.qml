import QtQuick 2.2
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import QtQuick 2.0

Item {
    Timer {
        interval: 200; running: true; repeat: true
		onTriggered: {
			var remaining_time = session_controller.get_remaining_time()
			if (remaining_time == '') {
				mainLoader.source = "welcome.qml"
			}
			remaining.text = remaining_time
		}
    }

	ColumnLayout {
		anchors.fill: parent

		Text {
			id: remaining
			text: 'running'
		}

		Button {
			Layout.alignment: Qt.AlignCenter
			text: "Abort"
			onClicked: {
				session_controller.stop_session()
				mainLoader.source = "welcome.qml"
			}
		}
	}
}
