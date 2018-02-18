import QtQuick 2.2
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

Item {
	ColumnLayout {
		anchors.fill: parent

		Text {
			text: 'Please select an action.'
		}

		Button {
			Layout.alignment: Qt.AlignCenter
			text: "List running sessions"
			onClicked: mainLoader.source = "session_list.qml"
			Keys.onPressed: {
				if (event.key == Qt.Key_Return) {
					mainLoader.source = "session_list.qml"
					event.accepted = true;
				}
			}
		}

		Button {
			Layout.alignment: Qt.AlignCenter
			text: "Start session"
			onClicked: {
				session_controller.start_session()
				mainLoader.source = "running_session.qml"
			}
		}
	}
}
