export function getElementById(elementId: string): HTMLElement {
  return document.getElementById(elementId)!;
}

export function readFile(
  inputElementId: string,
  successHandler: (fileReader: FileReader) => void
) {
  const reader = new FileReader();
  reader.readAsArrayBuffer(getFileById(inputElementId));
  reader.onloadend = () => {
    successHandler(reader);
  };
}

function getFileById(inputElementId: string): File {
  return (getElementById(inputElementId) as HTMLInputElement).files![0];
}

export function downloadAsTextFile(textContent: string, fileName: string) {
  const anchor = document.createElement("a");
  anchor.setAttribute("download", fileName);
  anchor.setAttribute(
    "href",
    "data:application/xml;charset=utf-8," + encodeURIComponent(textContent)
  );
  anchor.click();
}

