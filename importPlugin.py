import run
pluginId = 'plugin.data.run'
globals.thread.list[0] = [threading.Thread(target=plugin.run, args=pluginId), 0]