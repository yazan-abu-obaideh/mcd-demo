import { ReactElement } from "react";
import { McdInputForm } from "../FormsEnum";

type NavItemDescription = {
  form: McdInputForm;
  buttonInner: ReactElement;
};

const NAV_ITEMS: Array<NavItemDescription> = [
  { form: McdInputForm.SEEDS, buttonInner: <>Select rider</> },
  {
    form: McdInputForm.DIMENSIONS,
    buttonInner: <>Specify rider dimensions</>,
  },
  { form: McdInputForm.IMAGE, buttonInner: <>Upload rider image</> },
  {
    form: McdInputForm.TEXT,
    buttonInner: (
      <>
        Generate from Text Prompt <span className="text-warning">BETA</span>
      </>
    ),
  },
];

function NavItem(props: {
  buttonInner: ReactElement;
  setSelectedForm: () => void;
}): ReactElement {
  return (
    <li className="nav-item" onClick={() => props.setSelectedForm()}>
      <button type="button" className="nav-link">
        {props.buttonInner}
      </button>
    </li>
  );
}

export function FormSelectionNavBar(props: {
  setForm: (form: McdInputForm) => void;
}) {
  return (
    <div className="container border problem-form-tabs-div p-3">
      <ul className="nav">
        {NAV_ITEMS.map((navItemDesc) => (
          <NavItem
            buttonInner={navItemDesc.buttonInner}
            setSelectedForm={() => props.setForm(navItemDesc.form)}
          />
        ))}
      </ul>
    </div>
  );
}
