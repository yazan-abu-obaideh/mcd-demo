const { app, BrowserWindow } = require("electron");
const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  });

  win.loadFile("/home/yazan/Repositories/Personal/MCD-demo/frontend/web/dist/index.html");
};
app.whenReady().then(() => {
  createWindow();
});
