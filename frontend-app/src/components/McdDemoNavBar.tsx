import decode_logo from "../decode_logo.png";

export default function McdDemoNavBar() {
  return (
    <nav className="navbar navbar-expand-lg bg-light navbar-nav-scroll sticky-top bg-opacity-75">
      <div className="container-fluid">
        <a className="navbar-brand" href="#main-header">
          <img
            src={decode_logo}
            alt=""
            width="75"
            height="25"
            className="d-inline-block align-text-bottom"
          />
          Counterfactuals for Design
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <a
                className="nav-link active"
                aria-current="page"
                href="#generation-forms"
              >
                Interactive demo
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/mcd/read-more.html">
                Read more
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
