// all IDs here are deterministic

export function getBikeImgId(bikeId: string) {
  return `bike-img-${bikeId}`;
}
export function getBikeImagesDivId(bikeId: string) {
  return `bike-img-div-result-${bikeId}`;
}
export function getRenderBikeBtnId(bikeId: string) {
  return `render-bike-btn-${bikeId}`;
}
export function getDownloadBikeCadBtnId(bikeId: string) {
  return `download-cad-bike-btn-${bikeId}`;
}
