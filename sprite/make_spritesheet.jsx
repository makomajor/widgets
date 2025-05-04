#target photoshop

var docWidth = 2195;
var docHeight = 2195;
var columns = 9; // Anzahl Spalten im Spritesheet

var total = app.documents.length;
var rows = Math.ceil(total / columns);

// Neues Dokument erstellen für das Spritesheet
var spritesheet = app.documents.add(
  columns * docWidth,
  rows * docHeight,
  72,
  "Spritesheet",
  NewDocumentMode.RGB,
  DocumentFill.TRANSPARENT
);

// Bilder einfügen
for (var i = 0; i < total; i++) {
    var sourceDoc = app.documents[i];
    app.activeDocument = sourceDoc;

    sourceDoc.selection.selectAll();
    sourceDoc.selection.copy();

    app.activeDocument = spritesheet;
    var x = (i % columns) * docWidth;
    var y = Math.floor(i / columns) * docHeight;
    spritesheet.paste();
    spritesheet.activeLayer.translate(x, y);
}

// Zusammenführen (optional)
spritesheet.flatten();

// Speichern als PNG
var folder = Folder.selectDialog("Wähle einen Ordner zum Speichern des Spritesheets");
if (folder) {
    var file = new File(folder + "/spritesheet.png");
    var opts = new PNGSaveOptions();
    opts.compression = 9;
    spritesheet.saveAs(file, opts, true, Extension.LOWERCASE);
    alert("Spritesheet gespeichert!");
}