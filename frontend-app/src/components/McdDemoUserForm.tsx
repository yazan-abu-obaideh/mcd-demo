import { FormSelectionNavBar } from "./FormSelectionNavBar";
import { LandingHeader } from "./LandingHeader";
import { useState } from "react";
import { McdInputForm } from "../FormsEnum";
import { SeedsForm } from "./forms/SeedsForm";
import { UploadImageForm } from "./forms/UploadImageForm";
import { SpecifyRiderDimensionsForm } from "./forms/SpecifyRiderDimensionsForm";
import { GenerateFromTextForm } from "./forms/GenerateFromTextForm";
import { ServerResponseDiv } from "./ServerResponseDiv";
import { OptimizationRequestState } from "./McdServerResponse";

export default function McdDemoUserForm() {
  const [selectedForm, setSelectedForm] = useState(McdInputForm.SEEDS);
  const [serverResponse, setServerResponse] = useState(
    new OptimizationRequestState(undefined, false, undefined, undefined)
  );
  return (
    <div className="non-nav-body">
      <LandingHeader />
      <FormSelectionNavBar setForm={setSelectedForm} />
      <div id="generation-forms" className="container border rounded p-3 mb-3">
        {selectedForm === McdInputForm.SEEDS && (
          <SeedsForm setServerResponse={setServerResponse} />
        )}
        {selectedForm === McdInputForm.IMAGE && <UploadImageForm />}
        {selectedForm === McdInputForm.TEXT && <GenerateFromTextForm />}
        {selectedForm === McdInputForm.DIMENSIONS && (
          <SpecifyRiderDimensionsForm />
        )}
      </div>
      <ServerResponseDiv mcdServerResponse={serverResponse} />
    </div>
  );
}
