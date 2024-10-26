import { ReactElement } from "react";
import { McdInputForm } from "../FormsEnum";

function NavItem(props: { buttonInner: ReactElement | string; setSelectedForm: () => void }): ReactElement {
  return (
    <li className="nav-item" onClick={() => props.setSelectedForm()}>
      <button type="button" className="nav-link">
        {props.buttonInner}
      </button>
    </li>
  );
}

export function FormSelectionNavBar(props: { setForm: (form: McdInputForm) => void }) {
  return (
    <div className="container border problem-form-tabs-div p-3">
      <ul className="nav">
        <NavItem buttonInner={"Select rider"} setSelectedForm={() => props.setForm(McdInputForm.SEEDS)} />
        <NavItem
          buttonInner={"Specify rider dimensions"}
          setSelectedForm={() => props.setForm(McdInputForm.DIMENSIONS)}
        />
        <NavItem buttonInner={"Upload rider image"} setSelectedForm={() => props.setForm(McdInputForm.IMAGE)} />
        <NavItem
          buttonInner={
            <>
              Generate from Text Prompt <span className="text-warning">BETA</span>
            </>
          }
          setSelectedForm={() => props.setForm(McdInputForm.TEXT)}
        />
      </ul>
    </div>
  );
}
