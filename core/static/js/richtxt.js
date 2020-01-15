function enableEditMode () {
  richTextField.document.designMode = "On";
}

function execCmd (command) {
  richTextField.document.execCommand(command, flase, null);
}

function execCommandWithArg (command, arg) {
  richTextField.document.execCommand(command, flase, null);
}
