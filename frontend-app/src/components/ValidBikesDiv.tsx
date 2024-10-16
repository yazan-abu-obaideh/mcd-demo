import { McdServerResponse } from "./McdServerResponse";

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
                    <BikeActionButton innerText="Render Bike" />
                    <div style={{ height: "5px" }}></div>
                    <BikeActionButton innerText="Download CAD" />
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
function BikeActionButton(props: { innerText: string }) {
  return (
    <button className="btn btn-outline-danger btn-lg">{props.innerText}</button>
  );
}
