from controllers.GeneralController import GeneralController


def routes(sio):
    sio.on('connect')(GeneralController().connect)
    sio.on('disconnect')(GeneralController().disconnect)
