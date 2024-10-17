import { useState } from "react";
import { optimizationController } from "../declarative/client";
import { GeneratedBike } from "../declarative/controller";
import { McdServerResponse } from "./McdServerResponse";


const urlCreator = window.URL || window.webkitURL;

const ACTION_BUTTON_CSS = "btn btn-outline-danger btn-lg";
const DOWNLOAD_FAILED = { active: false, innerText: "Download failed" };
const DOWNLOAD_SUCCESSFUL = {
  active: false,
  innerText: "Downloaded successfully",
};
const DOWNLOADING = {
  active: false,
  innerText: "Downloading...",
};

type RenderingState = {
  renderingRequest: boolean;
};

function CarouselControl(props: { controlType: "prev" | "next" }) {
  return (
    <button
      className={"carousel-control-" + props.controlType}
      type="button"
      data-bs-target="#bikesCarousel"
      data-bs-slide={props.controlType}
    >
      <span
        className={`carousel-control-${props.controlType}-icon`}
        aria-hidden="true"
      ></span>
    </button>
  );
}

function BikeElement(props: {
  index: number;
  bike: { bike: GeneratedBike; bikePerformance: string };
}) {
  const [renderingState, setRenderingState] = useState({
    renderingRequested: false,
    renderingResult: undefined,
  });

  const active = props.index === 0 ? "active" : undefined;
  const className =
    "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div " +
    active;

  return (
    <div className={className}>
      <h4>Generated Bike {props.index + 1}</h4>
      <h5>{props.bike.bikePerformance}</h5>
      <br></br>
      <button onClick={() => {}} className={ACTION_BUTTON_CSS}>
        Render Bike
      </button>
      <div style={{ height: "5px" }}></div>
      <DownloadCadButton
        bike={props.bike.bike}
        bikePerformance={props.bike.bikePerformance}
      />
    </div>
  );
}

function DownloadCadButton(props: {
  bike: GeneratedBike;
  bikePerformance: string;
}) {
  const [buttonState, setButtonState] = useState({
    active: true,
    innerText: "Download CAD",
  });
  return (
    <button
      className={ACTION_BUTTON_CSS + (buttonState.active ? " " : " disabled")}
      onClick={() => {
        setButtonState(DOWNLOADING);
        const req = new GeneratedBike();
        req.bikeObject = props.bike;
        // TODO: req.seedImageId = "1";
        optimizationController
          .postDownloadBikeCadRequest(req)
          .then((res) => {
            if (res.status === 200) {
              res.text().then((resText) => {
                downloadTextFile(resText);
                setButtonState(DOWNLOAD_SUCCESSFUL);
              });
            } else {
              setButtonState(DOWNLOAD_FAILED);
            }
          })
          .catch(() => {
            setButtonState(DOWNLOAD_FAILED);
          });
      }}
    >
      {buttonState.innerText}
    </button>
  );
}

function downloadTextFile(resText: string) {
  const anchor = document.createElement("a");
  anchor.setAttribute("download", "bike.bcad");
  anchor.setAttribute(
    "href",
    "data:application/xml;charset=utf-8," + encodeURIComponent(resText)
  );
  anchor.click();
  anchor.remove();
}

export function ValidBikesDiv(props: { mcdServerResponse: McdServerResponse }) {
  return (
    <div id="response-received-div" className="p-3">
      <div id="bikesCarousel" className="carousel carousel-dark slide">
        <div
          id="generated-designs-consumer-carousel"
          className="carousel-inner"
        >
          <div>
            {props.mcdServerResponse.optimizationResponse?.bikes.map(
              (bike, index) => {
                return <BikeElement bike={bike} index={index} />;
              }
            )}
          </div>
        </div>
        <CarouselControl controlType="prev" />
        <CarouselControl controlType="next" />
      </div>
    </div>
  );
}

function BikeActionButton(props: { innerText: string; onClick: () => void }) {
  return (
    <button onClick={props.onClick} className={ACTION_BUTTON_CSS}>
      {props.innerText}
    </button>
  );
}
