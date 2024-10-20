function DropdownItem({
  itemText,
  onClickFun,
  extraClasses,
}: {
  itemText: string;
  onClickFun: () => void;
  extraClasses?: string;
}) {
  return (
    <li>
      <button type="button" className={"dropdown-item " + (extraClasses || "")} onClick={onClickFun}>
        {itemText}
      </button>
    </li>
  );
}

export function SubmitDropdown(props: {
  id: string;
  ergonomicOptimizationFunction: () => void;
  aerodynamicOptimizationFunction: () => void;
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
            <DropdownItem itemText="Ergonomic bikes!" onClickFun={() => props.ergonomicOptimizationFunction()} />
            <DropdownItem itemText="Aerodynamic bikes!" onClickFun={() => props.aerodynamicOptimizationFunction()} />
            <DropdownItem
              itemText="Structurally-optimal bikes! [COMING SOON]"
              onClickFun={() => {}}
              extraClasses="disabled"
            />
          </ul>
        </div>
      </div>
    </div>
  );
}
