import McdDemoNavBar from "../components/McdDemoNavBar";

export function ReadMore() {
  return (
    <>
      <McdDemoNavBar />
      <div className="non-nav-body">
        <div className="p-5 text-center">
          <div className="p-3" id="starting-point">
            <h2>What exactly is MCD?</h2>
            <p className="static-content-paragraph">
              The short answer is that MCD is a novel framework for counterfactual optimization in design problems. For
              the long answer, please refer to our
              <a href="https://arxiv.org/abs/2305.11308"> public access paper </a>
              or our
              <a href="https://github.com/Lyleregenwetter/Multiobjective-Counterfactuals-for-Design">
                open-source implementation of MCD{" "}
              </a>
              .
            </p>
          </div>
          <div className="p-3">
            <h2>What's actually happening in the interactive demo?</h2>
            <p className="static-content-paragraph">
              The chosen rider-bike combination is passed to MCD, which has been equipped with a method that evaluates
              ergonomic score/aerodynamic drag, depending on the type of optimization being performed. Riders are
              represented by 8 bodily dimensions, whereas bikes are represented by 14. MCD will attempt to produce as
              many unique, novel designs that meet specific performance targets, while also trying to keep generated
              designs as similar to the original bike as possible.
            </p>
          </div>
          <div className="p-3">
            <h2>What else can MCD be used for?</h2>
            <p className="static-content-paragraph">
              All sorts of design/optimization problems. MCD places no restrictions on parametric design representation,
              with integer, continuous, and categorical variables supported. MCD also places no restriction on the type
              of model used for performance predictions. This means MCD will work just as well with differentiable and
              non-differentiable machine learning models, as well as simulation or pure mathematical models.
            </p>
          </div>

          <div className="p-3">
            <h2>Care to provide a few examples?</h2>
            <p className="static-content-paragraph">Of course!</p>
            <h4>Multiobjective structural optimization</h4>
            <p className="inner-static-content-paragraph">
              Equipped with a machine learning model capable of predicting structural properties from 39 design
              parameters, MCD has been used to optimize bikes for properties such as weight and safety factor (i.e. the
              ratio of the maximum stress a bike can withstand to that of a typical loading scenario).
            </p>
            <h4>Cross-modal design recommendations with text prompts</h4>
            <p className="inner-static-content-paragraph">
              Making use of a Contrastive Language-Image Pretraining (CLIP) model, MCD was used to generate novel bike
              designs that resembled prompts such as 'A futuristic black cyberpunk-style road racing bicycle' and 'A
              sturdy compact bright blue mountain bike with thick tires'.
            </p>
          </div>

          <div className="p-3">
            <h2>Acknowledgements</h2>
            <p className="static-content-paragraph">
              We would like to thank Noah Wiley for his contributions to the image-to-rider-dimensions pipeline, as well
              as the ergonomic and aerodynamic performance prediction functions. We would also like to thank Amin
              Heyrani Nobari for his work on the bike rendering pipeline, and Brent Curry for allowing us to make use of
              the
              <a href="https://www.bikecad.ca/">BikeCAD</a> bicycle design software for this demo.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
