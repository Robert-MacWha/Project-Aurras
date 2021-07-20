const { contextBridge, ipcRenderer } = require("electron");
const ejs = require('ejs');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
    "api", {
        //send: (channel, data) => {
        request: (channel, data) => {
            let validChannels = ['titlebar', 'command_add', 'get'];
            if (validChannels.includes(channel)) {
                ipcRenderer.send(channel, data);
            }
        },
        respond: (channel, func) => {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        },
        ejs: ejs
    },
);