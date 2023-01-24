from controllers.AuthController import AuthController
from controllers.GeneralController import GeneralController
from controllers.MessageController import MessageController


def routes(sio):
    # Auth Routes
    sio.on('register_user')(AuthController().register)

    # General Routes
    sio.on('connect')(GeneralController().connect)
    sio.on('disconnect')(GeneralController().disconnect)

    # Messaging Routes
    sio.on('check_friend_phone')(GeneralController().check_friend_phone) # Add friends by number
    sio.on('get_friends')(GeneralController().get_friends)
    sio.on('send_message')(MessageController().send_message)
    sio.on('seen_message')(MessageController().seen_message) # Clients are chatting
    sio.on('seen_friend_message')(MessageController().seen_friend_messages) # After select friend
    sio.on('get_messages_history')(MessageController().get_messages_history) # After select friend



