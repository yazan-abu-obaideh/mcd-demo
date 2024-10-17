import { useState } from "react";
import { optimizationController } from "../declarative/client";
import { GeneratedBike } from "../declarative/controller";
import { McdServerResponse } from "./McdServerResponse";

const ACTION_BUTTON_CSS = "btn btn-outline-danger btn-lg";

export function ValidBikesDiv(props: { mcdServerResponse: McdServerResponse }) {
  return (
    <div id="response-received-div" className="p-3">
      <div id="carouselExampleDark" className="carousel carousel-dark slide">
        <div
          id="generated-designs-consumer-carousel"
          className="carousel-inner"
        >
          <div>
            {props.mcdServerResponse.optimizationResponse?.bikes.map(
              (b, index) => {
                console.log("Mapping bike with index " + index);
                const active = index === 0 ? "active" : undefined;
                const className =
                  "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div " +
                  active;
                return (
                  <div className={className}>
                    <h4>Generated Bike {index + 1}</h4>
                    <h5>{b.bikePerformance}</h5>
                    <br></br>
                    <BikeActionButton
                      onClick={() => {}}
                      innerText="Render Bike"
                    />
                    <div style={{ height: "5px" }}></div>
                    {DownloadCadButton(b)}
                  </div>
                );
              }
            )}
          </div>
        </div>
        <button
          className="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExampleDark"
          data-bs-slide="prev"
        >
          <span
            className="carousel-control-prev-icon"
            aria-hidden="true"
          ></span>
          <span className="visually-hidden">Previous</span>
        </button>
        <button
          className="carousel-control-next"
          type="button"
          data-bs-target="#carouselExampleDark"
          data-bs-slide="next"
        >
          <span
            className="carousel-control-next-icon"
            aria-hidden="true"
          ></span>
          <span className="visually-hidden">Next</span>
        </button>
      </div>
    </div>
  );
}
function DownloadCadButton(b: {
  bike: GeneratedBike;
  bikePerformance: string;
}) {
  const [buttonState, setButtonState] = useState({
    active: true,
    innerText: "Download CAD",
  });

  const extraClass = buttonState.active ? " " : " disabled";
  return (
    <button
      className={ACTION_BUTTON_CSS + extraClass}
      onClick={() => {
        b.bike.seedImageId = "1";
        const req = new GeneratedBike();
        req.bikeObject = b.bike;
        // TODO: req.seedImageId = "1";
        optimizationController
          .postDownloadBikeCadRequest(req)
          .then((res) => {
            if (res.status === 200) {
              res.text().then((resText) => {
                const anchor = document.createElement("a");
                anchor.setAttribute("download", "bike.xml");
                anchor.setAttribute(
                  "href",
                  "data:application/xml;charset=utf-8," +
                    encodeURIComponent(resText)
                );
                anchor.click();
                anchor.remove();
                setButtonState({
                  active: false,
                  innerText: "Download successful",
                });
              });
            }
          })
          .catch((err) => {
            setButtonState({ active: false, innerText: "Download failed" });
          });
      }}
    >
      {buttonState.innerText}
    </button>
  );
}

function BikeActionButton(props: { innerText: string; onClick: () => void }) {
  return (
    <button onClick={props.onClick} className={ACTION_BUTTON_CSS}>
      {props.innerText}
    </button>
  );
}
