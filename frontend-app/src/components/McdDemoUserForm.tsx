import {
  showForm,
  submitCustomRiderForm,
  submitRiderDimensionsForm,
  submitSeedsForm,
  submitTextPromptForm,
} from "../declerative/client";

import decodeLogo from "../assets/decode_logo.png"
import bike1 from "../assets/bike1.png";
import bike2 from "../assets/bike2.png";
import bike3 from "../assets/bike3.png";
import bike4 from "../assets/bike4.png";
import bike5 from "../assets/bike5.png";
import bike6 from "../assets/bike6.png";
import bike7 from "../assets/bike7.png";
import bike8 from "../assets/bike8.png";
import bike9 from "../assets/bike9.png";
import bike10 from "../assets/bike10.png";
import bike11 from "../assets/bike11.png";
import bike12 from "../assets/bike12.png";
import bike13 from "../assets/bike13.png";

import person1 from "../assets/person1.png"
import person2 from "../assets/person2.png"
import person3 from "../assets/person3.png"

export default function McdDemoUserForm() {
  return (
    <div className="non-nav-body">
      <div className="text-center m-5">
        <img
          className="d-block mx-auto mb-4"
          src={decodeLogo}
          alt=""
          width="225"
          height="82"
        />
        <h1 id="main-header" className="display-5 fw-bold text-body-emphasis">
          Multiobjective Counterfactuals for Design
        </h1>
        <div className="col-lg-6 mx-auto intro-paragraph">
          <p className="lead mb-4">
            MCD is an automated design recommendation framework that can help
            you generate performant and realistic designs. While this demo
            focuses on bike designs, MCD is a generic framework that can be
            configured to handle almost any design problem - regardless of the
            number or nature of constraints or objectives.
          </p>
          <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
            <div className="col">
              <div className="row justify-content-center m-1">
                <a
                  href="#generation-forms"
                  className="btn btn-outline-danger btn-lg px-4 gap-3 w-40"
                >
                  Generate CAD Designs
                </a>
              </div>
              <div className="row justify-content-center m-1">
                <a
                  href="/mcd/read-more.html"
                  className="btn btn-outline-danger btn-lg px-4 gap-3 w-40"
                >
                  Read more
                </a>
              </div>
            </div>
            <br />
          </div>
        </div>
      </div>
      <div className="container border problem-form-tabs-div p-3">
        <ul className="nav">
          <li className="nav-item" onClick={() => showForm("seeds-form-form")}>
            <button type="button" className="nav-link">
              Select rider
            </button>
          </li>
          <li
            className="nav-item"
            onClick={() => showForm("specify-rider-dimensions-form")}
          >
            <button type="button" className="nav-link">
              Specify rider dimensions
            </button>
          </li>
          <li
            className="nav-item"
            onClick={() => showForm("upload-rider-image-form")}
          >
            <button type="button" className="nav-link">
              Upload rider image
            </button>
          </li>
          <li
            className="nav-item"
            onClick={() => showForm("generate-from-text-form")}
          >
            <button type="button" className="nav-link">
              Generate from Text Prompt{" "}
              <span className="text-warning">[BETA]</span>
            </button>
          </li>
        </ul>
      </div>
      <div id="generation-forms" className="container border rounded p-3 mb-3">
        <form
          id="generate-from-text-form"
          className="m-3"
          style={{ display: "none" }}
        >
          <h3>Generate from Text Prompt</h3>
          <div className="row flex-cont">
            <div className="col-6">
              <input
                type="text"
                className="form-control"
                name="bike-description"
                id="bike-description-input"
                required
              />
              <label className="form-label" htmlFor="bike-description-input">
                Bike Description
              </label>
            </div>
          </div>
          <button
            className="btn btn-outline-danger"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#advancedOptions"
            aria-expanded="false"
            aria-controls="advancedOptions"
          >
            Show advanced options
          </button>
          <div className="collapse p-3" id="advancedOptions">
            <div className="row flex-cont">
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="optimizer_population"
                  id="optimizer_population-input"
                  min="1"
                  max="100"
                />
                <label
                  className="form-label"
                  htmlFor="optimizer_population-input"
                >
                  Bikes per generation
                </label>
              </div>
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="optimizer_generations"
                  max="60"
                  min="1"
                  id="optimizer_generations-input"
                />
                <label
                  className="form-label"
                  htmlFor="optimizer_generations-input"
                >
                  Number of generations
                </label>
              </div>
            </div>
            <div className="row flex-cont">
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="cosine_distance_upper_bound"
                  min="0.1"
                  max="1"
                  step="0.01"
                  id="cosine_distance_upper_bound-input"
                />
                <label
                  className="form-label"
                  htmlFor="cosine_distance_upper_bound-input"
                >
                  Cosine distance upper bound
                </label>
              </div>
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="avg_gower_weight"
                  step="0.01"
                  id="avg_gower_weight-input"
                />
                <label className="form-label" htmlFor="avg_gower_weight-input">
                  Average gower weight
                </label>
              </div>
            </div>
            <div className="row flex-cont">
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="cfc_weight"
                  step="0.01"
                  id="cfc_weight-input"
                />
                <label className="form-label" htmlFor="cfc_weight-input">
                  Counterfactual weight
                </label>
              </div>
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="gower_weight"
                  step="0.01"
                  id="gower_weight-input"
                />
                <label className="form-label" htmlFor="gower_weight-input">
                  Gower weight
                </label>
              </div>
            </div>
            <div className="row flex-cont">
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="diversity_weight"
                  step="0.01"
                  id="diversity_weight-input"
                />
                <label className="form-label" htmlFor="diversity_weight-input">
                  Divsersity weight
                </label>
              </div>
              <div className="col-6">
                <input
                  type="number"
                  className="form-control"
                  name="bonus_objective_weight"
                  step="0.01"
                  id="bonus_objective_weight-input"
                />
                <label
                  className="form-label"
                  htmlFor="bonus_objective_weight-input"
                >
                  Bonus objective weight
                </label>
              </div>
            </div>
            <div className="row flex-cont">
              <div className="col-6">
                <input
                  type="checkbox"
                  name="include_dataset"
                  id="include_dataset-input"
                />
                <label className="form-label" htmlFor="include_dataset-input">
                  Include dataset
                </label>
              </div>
            </div>
          </div>
          <div className="row flex-cont"></div>
          <div className="p-3">
            <div className="row flex-cont text-center justify-content-center">
              <button
                className="btn btn-outline-danger btn-lg w-40"
                type="button"
                id="generate-from-text-form-submit-button"
                onClick={() => submitTextPromptForm()}
              >
                Generate!
              </button>
            </div>
          </div>
        </form>
        <form id="seeds-form-form">
          <div id="person-image-container" className="m-3">
            <h3>Select Rider</h3>
            <div className="row p-5">
              <div className="col seed-bike-div">
                <img
                  className="seed-bike-img"
                  src={person1}
                  alt="rider-image-1"
                />
                <br />
                <input
                  id="rider-image-1"
                  value="1"
                  name="riderImage"
                  type="radio"
                  className="form-check-input"
                  checked
                  required
                />
                <label className="form-check-label" htmlFor="rider-image-1">
                  6'2"
                </label>
              </div>
              <div className="col seed-bike-div">
                <img
                  className="seed-bike-img"
                  src={person2}
                  alt="rider-image-2"
                />
                <br />
                <input
                  id="rider-image-2"
                  value="2"
                  name="riderImage"
                  type="radio"
                  className="form-check-input"
                  required
                />
                <label className="form-check-label" htmlFor="rider-image-2">
                  5'10"
                </label>
              </div>
              <div className="col seed-bike-div">
                <img
                  className="seed-bike-img"
                  src={person3}
                  alt="rider-image-3"
                />
                <br />
                <input
                  id="rider-image-3"
                  value="3"
                  name="riderImage"
                  type="radio"
                  className="form-check-input"
                  required
                />
                <label className="form-check-label" htmlFor="rider-image-3">
                  5'1"
                </label>
              </div>
            </div>
          </div>
          <div id="seeds-form-form-seed-bike-placeholder"></div>
          <div className="p-3">
            <div className="row flex-cont text-center justify-content-center">
              <div className="dropdown">
                <button
                  className="btn btn-outline-danger btn-lg dropdown-toggle w-40"
                  type="button"
                  id="dropdownMenuButton1"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Generate!
                </button>
                <ul
                  className="dropdown-menu w-40"
                  aria-labelledby="dropdownMenuButton1"
                >
                  <li>
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={() => submitSeedsForm("ergonomics")}
                    >
                      Ergonomic bikes!
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={() => submitSeedsForm("aerodynamics")}
                    >
                      Aerodynamic bikes!
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      className="dropdown-item disabled"
                      onClick={() => submitSeedsForm("aerodynamics")}
                    >
                      Structurally-optimal bikes! [COMING SOON]
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </form>
        <form id="upload-rider-image-form" style={{ display: "none" }}>
          <div id="upload-image-container" className="m-3">
            <h3>Upload Rider Image</h3>
            <div className="p-3">
              <div className="row flex-cont">
                <div className="col-6">
                  <input
                    className="form-control"
                    type="file"
                    accept=".jpg, .jpeg, .png, .svg"
                    id="user-img-upload"
                    name="user-img"
                    required
                  />
                </div>
              </div>

              <div className="row flex-cont">
                <div className="col-6">
                  <input
                    type="number"
                    className="form-control"
                    name="user-height"
                    id="user-height-input"
                    step="0.01"
                    required
                  />
                  <label className="form-label" htmlFor="user-height-input">
                    User Height (Inches)
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div id="upload-rider-image-form-seed-bike-placeholder"></div>
          <div className="p-3">
            <div className="row flex-cont text-center justify-content-center">
              <div className="dropdown">
                <button
                  className="btn btn-outline-danger btn-lg dropdown-toggle w-40"
                  type="button"
                  id="dropdownMenuButton1-upload-rider"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Generate!
                </button>
                <ul
                  className="dropdown-menu w-40"
                  aria-labelledby="dropdownMenuButton1"
                >
                  <li>
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={() => submitCustomRiderForm("ergonomics")}
                    >
                      Ergonomic bikes!
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={() => submitCustomRiderForm("aerodynamics")}
                    >
                      Aerodynamic bikes!
                    </button>
                  </li>
                  <li>
                    <button type="button" className="dropdown-item disabled">
                      Structurally-optimal bikes! [COMING SOON]
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </form>
        <form id="specify-rider-dimensions-form" style={{ display: "none" }}>
          <div id="specify-rider-dimensions-container" className="m-3">
            <h3>
              Specify rider dimensions
              <span style={{ fontSize: "small" }}>(Inches)</span>
            </h3>
            <div className="p-3">
              <div className="row flex-cont">
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="rider-height"
                    id="user-height-input-specify-rider-dimensions"
                    step="0.01"
                    value="73.5"
                    placeholder="73.5"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="user-height-input-specify-rider-dimensions"
                  >
                    Height
                  </label>
                </div>
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="shoulder-height"
                    id="shoulder-height-input"
                    step="0.01"
                    value="60"
                    placeholder="60"
                    required
                  />
                  <label className="form-label" htmlFor="shoulder-height-input">
                    Shoulder Height
                  </label>
                </div>
              </div>
              <div className="row flex-cont">
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="hip-ankle"
                    id="hip-ankle-input-specify-rider-dimensions"
                    step="0.01"
                    value="34"
                    placeholder="34"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="hip-ankle-input-specify-rider-dimensions"
                  >
                    Hip to Ankle
                  </label>
                </div>
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="hip-knee"
                    id="hip-knee-input-specify-rider-dimensions"
                    step="0.01"
                    value="16.5"
                    placeholder="16.5"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="hip-knee-input-specify-rider-dimensions"
                  >
                    Hip to Knee
                  </label>
                </div>
              </div>
              <div className="row flex-cont">
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="shoulder-wrist"
                    id="shoulder-wrist-input-specify-rider-dimensions"
                    step="0.01"
                    value="20.5"
                    placeholder="20.5"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="shoulder-wrist-input-specify-rider-dimensions"
                  >
                    Shoulder to wrist
                  </label>
                </div>
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="arm-length"
                    id="arm-length-input-specify-rider-dimensions"
                    step="0.01"
                    value="23.5"
                    placeholder="23.5"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="arm-length-input-specify-rider-dimensions"
                  >
                    Arm Length
                  </label>
                </div>
              </div>
              <div className="row flex-cont">
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="upper-leg"
                    id="upper-leg-input-specify-rider-dimensions"
                    step="0.01"
                    placeholder="16.5"
                    value="16.5"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="upper-leg-input-specify-rider-dimensions"
                  >
                    Upper Leg
                  </label>
                </div>
                <div className="col-3">
                  <input
                    type="number"
                    className="form-control"
                    name="lower-leg"
                    id="lower-leg-input-specify-rider-dimensions"
                    step="0.01"
                    value="20.25"
                    placeholder="20.25"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="lower-leg-input-specify-rider-dimensions"
                  >
                    Lower Leg
                  </label>
                </div>
              </div>
              <div className="row flex-cont">
                <div className="col-3" style={{ width: "50%" }}>
                  <input
                    type="number"
                    className="form-control"
                    name="torso-length"
                    id="torso-length-input-specify-rider-dimensions"
                    step="0.01"
                    placeholder="23"
                    value="23"
                    required
                  />
                  <label
                    className="form-label"
                    htmlFor="torso-length-input-specify-rider-dimensions"
                  >
                    Torso Length
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div id="specify-rider-dimensions-form-seed-bike-placeholder"></div>
          <div className="p-3">
            <div className="row flex-cont text-center justify-content-center">
              <div className="dropdown">
                <button
                  className="btn btn-outline-danger btn-lg dropdown-toggle w-40"
                  type="button"
                  id="dropdownMenuButton1-specify-rider-dimensions"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Generate!
                </button>
                <ul
                  className="dropdown-menu w-40"
                  aria-labelledby="dropdownMenuButton1"
                >
                  <li>
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={() => submitRiderDimensionsForm("ergonomics")}
                    >
                      Ergonomic bikes!
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={() => submitRiderDimensionsForm("aerodynamics")}
                    >
                      Aerodynamic bikes!
                    </button>
                  </li>
                  <li>
                    <button type="button" className="dropdown-item disabled">
                      Structurally-optimal bikes! [COMING SOON]
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </form>
      </div>
      <div
        id="server-response-div"
        className="container border rounded p-3"
        style={{ display: "none" }}
      >
        <h2>Generated Designs</h2>
        <div id="loading-or-result-div" className="container p-3">
          <div
            id="response-loading-div"
            className="text-center"
            style={{ display: "block" }}
          >
            <div className="spinner-border loading-element" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <div className="text-xl-center">
              <h4>MCD is generating designs...</h4>
              <h5>This should not take more than 30 seconds...</h5>
            </div>
          </div>
          <div
            id="response-received-div"
            className="p-3"
            style={{ display: "none" }}
          >
            <div
              id="carouselExampleDark"
              className="carousel carousel-dark slide"
            >
              <div
                id="generated-designs-consumer-carousel"
                className="carousel-inner"
              ></div>
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
          <div
            id="no-bikes-found-div"
            className="p-3 text-center"
            style={{ display: "none" }}
          >
            <h4>
              MCD could not generate any valid designs within the allotted time.
              Please try a different request.
            </h4>
          </div>
          <div
            id="error-response-div"
            className="p-3 text-center"
            style={{ display: "none" }}
          ></div>
        </div>
      </div>
    </div>
  );
}
