from controllers.AuthController import AuthController
from controllers.GeneralController import GeneralController
from controllers.MessageController import MessageController


def routes(sio):
    sio.on('connect')(GeneralController().connect)
    sio.on('disconnect')(GeneralController().disconnect)
    sio.on('register')(AuthController().register)
    sio.on('check_friend_phone')(GeneralController().check_friend_phone) # Add friends by number
    sio.on('get_friends')(GeneralController().get_friends)
    sio.on('send_message')(MessageController().send_message)



