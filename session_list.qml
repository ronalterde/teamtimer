import QtQuick 2.2
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

ColumnLayout {
	ListView {
		height: 100

		model: session_list_model
		delegate: Text {
			text: display
		}
	}

	Button {
		text: "Back"
		onClicked: mainLoader.source = "welcome.qml"
	}
}
