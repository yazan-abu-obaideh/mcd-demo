import { useState } from "react";
import { optimizationController, renderingController } from "../declarative/client";
import { GeneratedBike } from "../declarative/controller";
import { OptimizationRequestState } from "./McdServerResponse";
import { generateUuid } from "../declarative/generic_utils";
import bike1 from "../assets/bike1.png";
import bike2 from "../assets/bike2.png";
import bike3 from "../assets/bike3.png";
import bike5 from "../assets/bike5.png";
import bike6 from "../assets/bike6.png";
import bike7 from "../assets/bike7.png";
import bike10 from "../assets/bike10.png";
import bike11 from "../assets/bike11.png";
import bike12 from "../assets/bike12.png";
import "../styles.css";

const urlCreator = window.URL || window.webkitURL;

const SEED_ID_TO_IMAGE = new Map<string, string>();
SEED_ID_TO_IMAGE.set("1", bike1);
SEED_ID_TO_IMAGE.set("2", bike2);
SEED_ID_TO_IMAGE.set("3", bike3);
SEED_ID_TO_IMAGE.set("5", bike5);
SEED_ID_TO_IMAGE.set("6", bike6);
SEED_ID_TO_IMAGE.set("7", bike7);
SEED_ID_TO_IMAGE.set("10", bike10);
SEED_ID_TO_IMAGE.set("11", bike11);
SEED_ID_TO_IMAGE.set("12", bike12);

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
  renderingRequested: boolean;
  renderingResult: Blob | undefined;
  renderingFailed: boolean;
};

function CarouselControl(props: { controlType: "prev" | "next" }) {
  return (
    <button
      className={"carousel-control-" + props.controlType}
      type="button"
      data-bs-target="#bikesCarousel"
      data-bs-slide={props.controlType}
    >
      <span className={`carousel-control-${props.controlType}-icon`} aria-hidden="true"></span>
    </button>
  );
}

function BikeElement(props: {
  index: number;
  bike: { bike: GeneratedBike; bikePerformance: string };
  seedBikeId: string;
  isClips: boolean;
}) {
  const [renderingState, setRenderingState] = useState<RenderingState>({
    renderingRequested: false,
    renderingResult: undefined,
    renderingFailed: false,
  });

  const active = props.index === 0 ? "active" : undefined;
  const className = "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div " + active;

  const originalId = generateUuid();
  const renderedId = generateUuid();
  return (
    <div className={className}>
      <h4>Generated Bike {props.index + 1}</h4>
      <h5>{props.bike.bikePerformance}</h5>
      <br></br>
      {!renderingState.renderingRequested && (
        <button
          onClick={() => {
            setRenderingState({
              renderingRequested: true,
              renderingFailed: false,
              renderingResult: undefined,
            });

            const request = new GeneratedBike();
            request.bikeObject = props.bike.bike;
            request.bikePerformance = props.bike.bikePerformance;
            request.seedImageId = props.seedBikeId;

            const renderingFunction = props.isClips
              ? renderingController.postRenderClipsBikeRequest.bind(renderingController)
              : renderingController.postRenderBikeRequest.bind(renderingController);

            renderingFunction(request)
              .then((response) => {
                if (response.status !== 200) {
                  setRenderingState({
                    renderingRequested: true,
                    renderingFailed: true,
                    renderingResult: undefined,
                  });
                } else {
                  response.blob().then((resBlob) => {
                    setRenderingState({
                      renderingRequested: true,
                      renderingResult: resBlob,
                      renderingFailed: false,
                    });
                  });
                }
              })
              .catch(() => {
                setRenderingState({
                  renderingFailed: true,
                  renderingRequested: true,
                  renderingResult: undefined,
                });
              });
          }}
          className={ACTION_BUTTON_CSS}
        >
          Render Bike
        </button>
      )}
      {renderingState.renderingRequested && renderingState.renderingResult === undefined && (
        <div className="text-center bike-render-inner-element-div flex-column">
          <div className="spinner-border loading-element"></div>
          <div>Rendering bike...</div>
        </div>
      )}

      {renderingState.renderingResult !== undefined && (
        <div className="text-center p-5 row" style={{ display: "flex" }}>
          <div className="col bike-img-div-in-result">
            <img
              id={originalId}
              className="original-bike-img-in-result"
              alt="original bike"
              src={SEED_ID_TO_IMAGE.get(props.seedBikeId)}
            />
            <label style={{ display: "block" }} htmlFor={originalId}>
              Original
            </label>
          </div>
          <div className="col bike-img-div-in-result">
            <img
              id={renderedId}
              alt="rendered bike"
              className="rendered-bike-img"
              src={urlCreator.createObjectURL(renderingState.renderingResult)}
            />
            <label style={{ display: "block" }} htmlFor={renderedId}>
              Generated
            </label>
          </div>
        </div>
      )}

      {renderingState.renderingFailed && (
        <div className="bike-render-inner-element-div">
          <h4> Rendering failed... </h4>
        </div>
      )}

      <div style={{ height: "5px" }}></div>
      <DownloadCadButton
        bike={props.bike.bike}
        bikePerformance={props.bike.bikePerformance}
        seedBikeId={props.seedBikeId}
        isClips={props.isClips}
      />
    </div>
  );
}

function DownloadCadButton(props: {
  bike: GeneratedBike;
  bikePerformance: string;
  seedBikeId: string;
  isClips: boolean;
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
        req.seedImageId = props.seedBikeId;

        const downloadBikeFunction = props.isClips
          ? optimizationController.postDownloadClipsBikeCadRequest.bind(optimizationController)
          : optimizationController.postDownloadBikeCadRequest.bind(optimizationController);

        downloadBikeFunction(req)
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
          .catch((err) => {
            setButtonState(DOWNLOAD_FAILED);
            throw err;
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
  anchor.setAttribute("href", "data:application/xml;charset=utf-8," + encodeURIComponent(resText));
  anchor.click();
  anchor.remove();
}

export function ValidBikesDiv(props: { mcdServerResponse: OptimizationRequestState }) {
  return (
    <div id="response-received-div" className="p-3">
      <div id="bikesCarousel" className="carousel carousel-dark slide">
        <div id="generated-designs-consumer-carousel" className="carousel-inner">
          <div>
            {props.mcdServerResponse.optimizationResponse?.bikes.map((bike, index) => {
              return (
                <BikeElement
                  isClips={props.mcdServerResponse.isClips}
                  seedBikeId={props.mcdServerResponse.requestPayload!.seedBike}
                  bike={bike}
                  index={index}
                />
              );
            })}
          </div>
        </div>
        <CarouselControl controlType="prev" />
        <CarouselControl controlType="next" />
      </div>
    </div>
  );
}
