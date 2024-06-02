import { getElementById } from "./html_utils";

export class ExclusivelyVisibleElements {
  // a class that encapsulates the logic of a bunch of elements where only one can be visible at a time
  constructor(elementIds: Array<string>) {
    this.elementIds = elementIds;
  }

  elementIds: Array<string>;
  showElement(id: string, elementDisplay = "block") {
    if (!this.elementIds.includes(id)) {
      throw Error("Element not found");
    }
    this.elementIds.forEach((elementId) => {
      getElementById(elementId).setAttribute("style", "display: none");
    });
    getElementById(id).setAttribute("style", `display: ${elementDisplay}`);
  }
}