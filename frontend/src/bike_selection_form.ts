export function getSeedBikeSelectionHtml(idSuffix: string) {
  return `<div id="seed-bike-selection-container${idSuffix}" class="m-3">
    <h3>Select Seed Bike</h3>
    <div id="bikes-container${idSuffix}" class="m-3"></div>
    <div id="all-bikes-helper-div${idSuffix}">
        <div class="row p-5">
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike1.png"
                        alt="seed-bike-1"
                />
                <br/>
                <input
                        id="seed1${idSuffix}"
                        value="1"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed1${idSuffix}"
                >Snow Camo</label
                >
            </div>
    
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike2.png"
                        alt="seed-bike-2"
                />
                <br/>
                <input
                        id="seed2${idSuffix}"
                        value="2"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed2${idSuffix}"
                >Childlike</label
                >
            </div>
    
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike3.png"
                        alt="seed-bike-3"
                />
                <br/>
                <input
                        id="seed3${idSuffix}"
                        value="3"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed3${idSuffix}"
                >Fiery</label
                >
            </div>
        </div>
    
        <div class="row p-5">
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike11.png"
                        alt="seed-bike-11"
                />
                <br/>
                <input
                        id="seed11${idSuffix}"
                        value="11"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed11${idSuffix}"
                >Pythonic</label
                >
            </div>
    
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike5.png"
                        alt="seed-bike-5"
                />
                <br/>
                <input
                        id="seed5${idSuffix}"
                        value="5"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed5${idSuffix}"
                >Inferno</label
                >
            </div>
    
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike6.png"
                        alt="seed-bike-6"
                />
                <br/>
                <input
                        id="seed6${idSuffix}"
                        value="6"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed6${idSuffix}"
                >Wintery</label
                >
            </div>
        </div>
        <div class="row p-5">
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike7.png"
                        alt="seed-bike-7"
                />
                <br/>
                <input
                        id="seed7${idSuffix}"
                        value="7"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed7${idSuffix}"
                >Pastel</label
                >
            </div>
    
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike10.png"
                        alt="seed-bike-10"
                />
                <br/>
                <input
                        id="seed10${idSuffix}"
                        value="10"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed10${idSuffix}"
                >Standard</label
                >
            </div>
    
            <div class="col seed-bike-div">
                <img
                        class="seed-bike-img"
                        src="../assets/bike12.png"
                        alt="seed-bike-12"
                />
                <br/>
                <input
                        id="seed12${idSuffix}"
                        value="12"
                        name="seedBike"
                        type="radio"
                        class="form-check-input"
                        required
                />
                <label class="form-check-label" for="seed12${idSuffix}"
                >Sleek</label
                >
            </div>
        </div>
    </div>
    </div>`;
}
