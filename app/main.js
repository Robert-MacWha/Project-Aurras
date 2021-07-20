const { app, BrowserWindow, ipcMain  } = require('electron');

const ejse = require('ejs-electron')
const path = require('path');
const Store = require('./store.js');

//? load in the data from the file system
let store = new Store();
let { entities, intents, prompts, global_id } = store.load();

// set the ejs data to the loaded data
ejse.data({'entities': entities, 'intents': intents, 'prompts': prompts});

//? app functions
let mainWindow;

// create the application window and load the index html file
function createWindow () {

    mainWindow = new BrowserWindow({
        width: 1000,
        height: 600,
        minWidth: 900,
        minHeight: 600,
        frame: false,
        webPreferences: {
            nodeIntegration: false, // is default value after Electron v5
            contextIsolation: true, // protect against prototype pollution
            enableRemoteModule: false, // turn off remote
            preload: path.join(app.getAppPath(), 'preload.js') // use a preload script
          }
    });
  
    mainWindow.loadFile(path.join(app.getAppPath(), 'public/html/index.ejs'));
}

//? app lifecycle
// start the app
app.whenReady().then(createWindow);

// close the app
app.on('window-all-closed', () => {
    app.quit();
});

//? IPC communication between main and frontend - https://stackoverflow.com/questions/44008674/how-to-import-the-electron-ipcrenderer-in-a-react-webpack-2-setup
// titlebar communications
ipcMain.on('titlebar', (e, args) => {

    // parce window management code
    if      (args == 'exit')     app.quit();
    else if (args == 'minimize') mainWindow.minimize();
    else if (args == 'maximize') mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize();
    
});

// command management communication (adding entities, intents, and prompts)
ipcMain.on('command_add', (e, args) => {

    // re-format the provided command (add an id, remove the type)
    args.id = global_id += 1;

    let type = args.type;
    delete args.type;

    // if there is an entity array, replace the strings with objects
    if ('entities' in args) {
        for(let i = args.entities.length - 1; i >= 0; i --) {

            let valid = false;
            for(const [key, value] of Object.entries(entities)) {

                if (value.name == args.entities[i]) {
                    args.entities[i] = value.id;
                    valid = true;
                }
            }

            if (!valid) {
                console.log('Invalid: ', args.entities[i], i);
                args.entities.pop(i);
            }

        }
    }

    // add the data to the arrays
    if      (type == 'entities') entities[args.id] = args;
    else if (type == 'intents')  intents[args.id] = args;
    else if (type == 'prompts')  prompts[args.id] = args;
    
    // save the new data
    store.save(entities, intents, prompts, global_id);

    // update the ejs data for the frontend
    ejse.data({'entities': entities, 'intents': intents, 'prompts': prompts});
    
});