/**
 * Interview Ace — Electron Main Process
 *
 * Creates a frameless, always-on-top overlay window.
 * The window is transparent and click-through when not focused,
 * so it can float over video call apps (Zoom, Teams, Meet).
 */

const { app, BrowserWindow, ipcMain, globalShortcut } = require("electron");
const path = require("path");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 400,
    height: 600,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: true,
    skipTaskbar: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  // Load Vite dev server in development, built files in production
  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:3000");
    mainWindow.webContents.openDevTools({ mode: "detach" });
  } else {
    mainWindow.loadFile(path.join(__dirname, "../dist/index.html"));
  }
}

app.whenReady().then(() => {
  createWindow();

  // Global shortcut to toggle visibility (Ctrl+Shift+I)
  globalShortcut.register("CommandOrControl+Shift+I", () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
    }
  });
});

app.on("window-all-closed", () => {
  globalShortcut.unregisterAll();
  if (process.platform !== "darwin") app.quit();
});

// IPC handlers for frontend communication
ipcMain.handle("toggle-always-on-top", () => {
  const isOnTop = mainWindow.isAlwaysOnTop();
  mainWindow.setAlwaysOnTop(!isOnTop);
  return !isOnTop;
});

ipcMain.handle("set-opacity", (_, opacity) => {
  mainWindow.setOpacity(opacity);
});
