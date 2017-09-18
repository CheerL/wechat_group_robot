import electron from 'electron'
/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
    global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

const app = electron.app
const BrowserWindow = electron.BrowserWindow
const globalShortcut = electron.globalShortcut
const Tray = electron.Tray
const Menu = electron.Menu
const ipcMain = electron.ipcMain
const winURL = process.env.NODE_ENV === 'development' ?
    `http://localhost:9080` :
    `file://${__dirname}/index.html`
const cmd = process.env.NODE_ENV === 'development' ?
    `${__dirname}\\..\\..\\build\\api\\group_robot_api.exe` :
    `${__dirname}\\..\\..\\..\\api\\group_robot_api.exe`
const icon = process.env.NODE_ENV === 'development' ?
    `${__dirname}\\..\\..\\build\\icons\\icon.ico` :
    `${__dirname}\\..\\..\\..\\icons\\icon.ico`
const spawn = require('child_process').spawn
const exec = require('child_process').exec

let myWindow = null

const shouldQuit = app.makeSingleInstance((commandLine, workingDirectory) => {
    if (myWindow) {
        if (myWindow.isMinimized()) {
            myWindow.restore()
        }
        myWindow.focus()
    }
})

if (shouldQuit) {
    app.quit()
}
let mainWindow
let appIcon
let contextMenu
spawn(cmd)

function createWindow() {
    /**
     * Initial window options
     */

    mainWindow = new BrowserWindow({
            height: 700,
            useContentSize: true,
            width: 1000,
            resizable: true,
            webPreferences: { webSecurity: false }
        })
        // mainWindow.openDevTools()
    mainWindow.loadURL(winURL)
    mainWindow.setMenu(null)
    mainWindow.on('closed', () => {
        mainWindow = null
    })

    appIcon = new Tray(icon)
    contextMenu = Menu.buildFromTemplate([{
            label: '隐藏窗口',
            click: item => {
                item.visible = false
                item.menu.items[1].visible = true
                mainWindow.hide()
            }
        },
        {
            label: '显示窗口',
            visible: false,
            click: item => {
                item.visible = false
                item.menu.items[0].visible = true
                mainWindow.show()
            }
        }, {
            label: '退出',
            click: () => {
                mainWindow.close()
                appIcon.destroy()
            }
        },
    ]);
    appIcon.setToolTip('微信群转发助手');
    appIcon.setContextMenu(contextMenu);
}

app.on('ready', () => {
    createWindow()
    globalShortcut.register('CmdOrCtrl+Alt+D', () => {
        mainWindow.openDevTools()
    })
})

app.on('window-all-closed', () => {
    exec(`\"${cmd}\" end`, () => {
        if (process.platform !== 'darwin') {
            app.quit()
        }
    })
})

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow()
    }
})


// Tray.on('click', () => {
//         appIcon.displayBalloon()
//     })
/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */