/*
FILE HEADER
*/

/*
*/
function readInputFile(fileField){
    const fileReader = new FileReader();
    fileReader.onload = event => return event.target.result;
    reader.onerror = error => reject(error);
    reader.readAsText(fileField);
}
