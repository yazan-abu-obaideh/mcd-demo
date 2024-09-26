import bike1 from "../assets/bike1.png";
import bike2 from "../assets/bike2.png";
import bike3 from "../assets/bike3.png";
import bike5 from "../assets/bike5.png";
import bike6 from "../assets/bike6.png";
import bike7 from "../assets/bike7.png";
import bike10 from "../assets/bike10.png";
import bike11 from "../assets/bike11.png";
import bike12 from "../assets/bike12.png";
import { PropsWithChildren, ReactElement } from "react";

type BikeDivDescription = {
  imageSrc: string;
  inputValue: string;
  labelText: string;
};

const FIRST_ROW: Array<BikeDivDescription> = [
  { imageSrc: bike1, inputValue: "1", labelText: "Snow Camo" },
  { imageSrc: bike2, inputValue: "2", labelText: "Childlike" },
  { imageSrc: bike3, inputValue: "3", labelText: "Fiery" },
];

const SECOND_ROW: Array<BikeDivDescription> = [
  { imageSrc: bike11, inputValue: "11", labelText: "Pythonic" },
  { imageSrc: bike5, inputValue: "5", labelText: "Inferno" },
  { imageSrc: bike6, inputValue: "6", labelText: "Wintery" },
];

const THIRD_ROW: Array<BikeDivDescription> = [
  { imageSrc: bike7, inputValue: "7", labelText: "Pastel" },
  { imageSrc: bike10, inputValue: "10", labelText: "Standard" },
  { imageSrc: bike12, inputValue: "12", labelText: "Sleek" },
];

function SeedBikeDiv(props: {
  idSuffix: string;
  imageSrc: string;
  inputValue: string;
  labelText: string;
}): ReactElement {
  const seedId = "seed".concat(props.inputValue);
  return (
    <div className="col seed-bike-div">
      <img
        className="seed-bike-img"
        src={props.imageSrc}
        alt="seed-bike-image"
      />
      <br />
      <input
        id={`${seedId}${props.idSuffix}`}
        value={props.inputValue}
        name="seedBike"
        type="radio"
        className="form-check-input"
        required
      />
      <label
        className="form-check-label"
        htmlFor={`${seedId}${props.idSuffix}`}
      >
        {props.labelText}
      </label>
    </div>
  );
}

function BikesRow(props: PropsWithChildren): ReactElement {
  return <div className="row p-5">{props.children}</div>;
}

function toElements(
  idSuffix: string,
  elementDescriptions: Array<BikeDivDescription>
): Array<ReactElement> {
  return elementDescriptions.map((elemDesc) => (
    <SeedBikeDiv
      idSuffix={idSuffix}
      imageSrc={elemDesc.imageSrc}
      labelText={elemDesc.labelText}
      inputValue={elemDesc.inputValue}
    />
  ));
}

export default function BikeSelectionForm(props: { idSuffix: string }) {
  return (
    <div id={`seed-bike-selection-container${props.idSuffix}`} className="m-3">
      <h3>Select Seed Bike</h3>
      <div id={`bikes-container${props.idSuffix}`} className="m-3"></div>
      <div id={`all-bikes-helper-div${props.idSuffix}`}>
        <BikesRow>{toElements(props.idSuffix, FIRST_ROW)}</BikesRow>
        <BikesRow>{toElements(props.idSuffix, SECOND_ROW)}</BikesRow>
        <BikesRow>{toElements(props.idSuffix, THIRD_ROW)}</BikesRow>
      </div>
    </div>
  );
}
