import { ReactElement } from "react";
import decodeLogo from "../assets/decode_logo.png";

function DecodeLogo() {
  return (
    <img
      className="d-block mx-auto mb-4"
      src={decodeLogo}
      alt=""
      width="225"
      height="82"
    />
  );
}

function IntroParagraph() {
  return (
    <p className="lead mb-4">
      MCD is an automated design recommendation framework that can help you
      generate performant and realistic designs. While this demo focuses on bike
      designs, MCD is a generic framework that can be configured to handle
      almost any design problem - regardless of the number or nature of
      constraints or objectives.
    </p>
  );
}

function MainHeader() {
  return (
    <h1 id="main-header" className="display-5 fw-bold text-body-emphasis">
      Multiobjective Counterfactuals for Design
    </h1>
  );
}

function ActionLink(props: { href: string; visibleText: string }) {
  return (
    <div className="row justify-content-center m-1">
      <a
        href={props.href}
        className="btn btn-outline-danger btn-lg px-4 gap-3 w-40"
      >
        {props.visibleText}
      </a>
    </div>
  );
}

export function LandingHeader(): ReactElement {
  return (
    <div className="text-center m-5">
      <DecodeLogo />
      <MainHeader />
      <div className="col-lg-6 mx-auto intro-paragraph">
        <IntroParagraph />
        <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
          <div className="col">
            <ActionLink
              href="#generation-forms"
              visibleText="Generate CAD Designs"
            />
            <ActionLink href="/mcd/read-more.html" visibleText="Read more" />
          </div>
          <br />
        </div>
      </div>
    </div>
  );
}
