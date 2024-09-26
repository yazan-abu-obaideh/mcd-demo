import { ReactElement } from "react";
import { showForm } from "../declerative/client";

type NavItemDescription = {
  formId: string;
  buttonInner: ReactElement;
};

const NAV_ITEMS: Array<NavItemDescription> = [
  { formId: "seeds-form-form", buttonInner: <>Select rider</> },
  {
    formId: "specify-rider-dimensions-form",
    buttonInner: <>Specify rider dimensions</>,
  },
  { formId: "upload-rider-image-form", buttonInner: <>Upload rider image</> },
  {
    formId: "generate-from-text-form",
    buttonInner: (
      <>
        Generate from Text Prompt <span className="text-warning">BETA</span>
      </>
    ),
  },
];

function NavItem(props: {
  formId: string;
  buttonInner: ReactElement;
}): ReactElement {
  return (
    <li className="nav-item" onClick={() => showForm(props.formId)}>
      <button type="button" className="nav-link">
        {props.buttonInner}
      </button>
    </li>
  );
}

export function FormSelectionNavBar() {
  return (
    <div className="container border problem-form-tabs-div p-3">
      <ul className="nav">
        {NAV_ITEMS.map((navItemDesc) => (
          <NavItem
            formId={navItemDesc.formId}
            buttonInner={navItemDesc.buttonInner}
          />
        ))}
      </ul>
    </div>
  );
}
