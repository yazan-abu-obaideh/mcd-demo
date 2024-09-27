export function SubmitDropdown(props: {
    id: string;
    typedSubmissionFunction: (optimizationType: string) => void;
  }) {
    const buttonId = "dropdownMenuButton" + props.id;
    return (
      <div className="p-3">
        <div className="row flex-cont text-center justify-content-center">
          <div className="dropdown">
            <button
              className="btn btn-outline-danger btn-lg dropdown-toggle w-40"
              type="button"
              id={buttonId}
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Generate!
            </button>
            <ul className="dropdown-menu w-40" aria-labelledby={buttonId}>
              <li>
                <button
                  type="button"
                  className="dropdown-item"
                  onClick={() => props.typedSubmissionFunction("ergonomics")}
                >
                  Ergonomic bikes!
                </button>
              </li>
              <li>
                <button
                  type="button"
                  className="dropdown-item"
                  onClick={() => props.typedSubmissionFunction("aerodynamics")}
                >
                  Aerodynamic bikes!
                </button>
              </li>
              <li>
                <button
                  type="button"
                  className="dropdown-item disabled"
                  onClick={() => {}}
                >
                  Structurally-optimal bikes! [COMING SOON]
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
  