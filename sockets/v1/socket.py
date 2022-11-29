from controllers.AuthController import AuthController
from controllers.GeneralController import GeneralController


def routes(sio):
    sio.on('connect')(GeneralController().connect)
    sio.on('disconnect')(GeneralController().disconnect)
    sio.on('register')(AuthController().register)
    sio.on('check_friend_phone')(GeneralController().check_friend_phone)

