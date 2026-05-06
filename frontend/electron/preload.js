/**
 * Interview Ace — Electron Preload Script
 *
 * Exposes safe IPC bridges to the renderer process.
 * Uses contextIsolation for security.
 */

const { contextBridge, ipcMain } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  toggleAlwaysOnTop: () => ipcRenderer.invoke("toggle-always-on-top"),
  setOpacity: (opacity) => ipcRenderer.invoke("set-opacity", opacity),
});
