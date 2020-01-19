function enableEditMode () {
  richTextField.document.designMode = "On";
}

function execCmd (command) {
  richTextField.document.execCommand(command, false, null);
}

function execCommandWithArg (command, arg) {
  richTextField.document.execCommand(command, false, null);
}

function somefunc() {
  document.getElementById("id_body").contentWindow.document;
}

function anotheryetsomefunc () {
  document.querySelector('input').value = somefunc();
}

anotheryetsomefunc();
