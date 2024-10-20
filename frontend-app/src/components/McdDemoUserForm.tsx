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

const INITIAL_RESPONSE_STATE = new OptimizationRequestState(false, undefined, false, undefined, undefined);

export default function McdDemoUserForm() {
  const [selectedForm, setSelectedForm] = useState(McdInputForm.SEEDS);
  const [serverResponse, setServerResponse] = useState(INITIAL_RESPONSE_STATE);
  return (
    <div className="non-nav-body">
      <LandingHeader />
      <FormSelectionNavBar setForm={setSelectedForm} />
      <div id="generation-forms" className="container border rounded p-3 mb-3">
        {selectedForm === McdInputForm.SEEDS && <SeedsForm setServerResponse={setServerResponse} />}
        {selectedForm === McdInputForm.IMAGE && <UploadImageForm setServerResponse={setServerResponse} />}
        {selectedForm === McdInputForm.TEXT && <GenerateFromTextForm />}
        {selectedForm === McdInputForm.DIMENSIONS && (
          <SpecifyRiderDimensionsForm setServerResponse={setServerResponse} />
        )}
      </div>

      {serverResponse.started && <ServerResponseDiv mcdServerResponse={serverResponse} />}
    </div>
  );
}
