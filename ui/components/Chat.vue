<template>
  <div class="body">
    <b-modal
      id="add"
      title="Add your friend"
      hide-footer
      @hide="
        friendInfo = false;
        friendPhoneNumber = '';
        beforeAdded = false;
      "
    >
      <div v-if="!friendInfo">
        <div style="min-height: 200px">
          <div style="min-height: 100px; width: 90%">
            <div class="input-group">
              <label for=""
                ><i style="font-size: 17pt" class="fa fa-mobile mt-3 pt-1"></i
              ></label>
              <input
                v-model="friendPhoneNumber"
                style="margin: 0 !important"
                type="text"
                class="form-control"
                placeholder="Enter your friend's phone number"
                aria-label="Username"
                aria-describedby="basic-addon1"
              />
            </div>
          </div>
        </div>
        <div class="btn-group float-right" style="min-height: 50px">
          <button style="height: 30px" class="btn btn-secondary fa fa-times"></button>
          <button
            style="height: 30px"
            class="btn btn-success fa fa-check"
            @click="checkFriend()"
          ></button>
        </div>
      </div>
      <div v-else style="position: relative; min-height: 100px">
        <div v-if="friendsExist && !beforeAdded" class="jumbotron bg-success text-light">
          congratulations! <b>{{ friendName }}</b> added to your friends list
          successfully. :)
        </div>
        <div v-if="beforeAdded" class="jumbotron bg-secondary text-light">
          Sorry! <b>{{ friendPhoneNumber }}</b> is added before in your friends list.
        </div>
        <div
          v-if="!friendsExist && !beforeAdded"
          class="jumbotron bg-secondary text-light"
        >
          Sorry! <b>{{ friendPhoneNumber }}</b> is not registered in instant messanger :(
        </div>
        <div style="position: absolute; bottom: 0px; right: 0; min-height: 40px">
          <button class="btn btn-primary mt-4" @click="$bvModal.hide('add')">OK</button>
        </div>
      </div>
    </b-modal>

    <!--It's just a concept, a chat UI design for direct messaging!
Enjoy! :) Don't forget to click the heart if you like it! -->

    <div class="container">
      <div
        class="chatbox-disabled d-flex justify-content-center align-items-center"
        v-if="!selectedFriend"
      >
        <p class="bg-success p-3" style="opacity: 0.5; border-radius: 5px">
          Select a chat or friend.
        </p>
      </div>
      <div class="chatbox" v-if="selectedFriend">
        <div class="top-bar">
          <div class="avatar">
            <p>{{ selectedFriend.name.slice(0, 1) }}</p>
          </div>
          <div class="name">{{ selectedFriend.name }}</div>
          <div class="icons">
            <i class="fas fa-phone"></i>
            <i class="fas fa-video"></i>
          </div>
          <div class="menu">
            <div class="dots"></div>
          </div>
        </div>
        <div class="middle" ref="cont">
          <div
            v-for="msg in selectedMessages"
            :key="msg.id != 'Sending' ? msg.id : msg.index"
          >
            <div :class="msg.type == 'r' ? 'in d-flex bubble' : 'out d-flex'">
              <small
                v-if="msg.type == 'r'"
                style="position: absolute; right: 15px; bottom: 1px"
                >{{ momentDate(msg.created) }}</small
              >

              <div v-if="msg.type == 's'" style="min-width: 50%"></div>
              <div
                style="position: relative; padding-bottom: 20px"
                :class="msg.type == 's' ? 'bubble' : ''"
                :style="
                  msg.type == 's'
                    ? {
                        background: '#2176FF',
                        'min-width': '50%',
                        color: 'white',
                      }
                    : ''
                "
              >
                <div>
                  {{ msg.message }}
                  <span
                    v-if="msg.type == 's'"
                    style="position: absolute; right: 15px; bottom: 1px"
                  >
                    <small v-if="msg.id != 'Sending'" style="background: graysmoke">{{
                      msg.created
                    }}</small>
                    <i v-if="msg.id != 'Sending' && !msg.seen" class="fa fa-check"></i>
                    <i
                      v-if="msg.id != 'Sending' && msg.seen"
                      class="fa fa-check-double"
                    ></i>
                    <i v-if="msg.id == 'Sending'" class="fa fa-circle-notch fa-spin"></i>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bottom-bar">
          <div class="chat">
            <input
              @keyup.enter="sendMessage()"
              v-model="message"
              type="text"
              placeholder="Type a message..."
            />
            <img
              src="../static/send.png"
              style="
                height: 20px;
                width: 20px;
                position: absolute;
                right: 15px;
                top: 15px;
                transform: rotate(0deg);
                cursor: pointer;
              "
              alt=""
            />
            <!-- <button type="submit"><i class="fas fa-paper-plane"></i></button> -->
          </div>
        </div>
      </div>
      <div class="messages" style="position: relative">
        <button
          @click="$bvModal.show('add')"
          style="
            position: absolute;
            left: 5px;
            top: 5px;
            width: 50px;
            height: 50px;
            border-radius: 100%;
          "
          class="btn btn-primary"
        >
          <i class="fa fa-user-plus"></i>
        </button>
      </div>
      <div class="profile">
        <div class="avatar">
          <p>{{ user.name.slice(0, 1) }}</p>
        </div>
        <div class="name2">
          {{ user.name }}
          <p class="email">{{ user.phone_number }}</p>
        </div>
      </div>
      <ul class="people">
        <li
          @click="selectFriend(friend)"
          v-for="(friend, index) in friends"
          :key="friend.phoneNumber"
          class="person"
          :class="friend == selectedFriend ? 'focus' : ''"
        >
          <span class="title">{{ friend.name }} </span>
          <span
            class="time"
            v-if="friendsListInfo.length > 0 && friendsListInfo[index].created"
            >{{ momentDate(friendsListInfo[index].created) }}</span
          ><br />
          <div
            style="
              position: absolute;
              background: #2176ff;
              width: 20px;
              height: 20px;
              border-radius: 100%;
              right: -10px;
              text-align: center;
              padding-top: 4px;
            "
            v-if="friendsListInfo.length > 0 && friendsListInfo[index].unreads > 0"
          >
            <span style="padding-top: 10px; font-size: 0.8em; color: white">
              {{ friendsListInfo[index].unreads }}
            </span>
          </div>
          <span class="preview">{{
            friendsListInfo.length > 0
              ? friendsListInfo[index].lastMessage
              : "Start messaging"
          }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "App",
  props: ["socket", "user", "friends", "history"],
  data() {
    return {
      friendInfo: false,
      friendPhoneNumber: "",
      friendName: "",
      friendsExist: false,
      friendsListInfo: [],
      beforeAdded: false,
      selectedFriend: "",
      selectedMessages: [],
      message: "",
      messages: [],
    };
  },
  methods: {
    momentDate(d) {
      return moment.utc(d).local().format("HH:mm A");
    },
    selectFriend(friend) {
      if (friend.id == this.selectedFriend.id) return;
      this.selectedMessages = [];
      this.selectedFriend = friend;
      let index = this.getIndexOfFriend(this.selectedFriend.id);
      this.friendsListInfo[index].unreads = 0;
      this.messages.map((msg) => {
        if (msg.from == this.selectedFriend.id || msg.to == this.selectedFriend.id) {
          this.selectedMessages.push(msg);
        }
      });
      this.socket.emit("seen_friend_message", this.selectedFriend.id);
    },
    sendMessage() {
      let msg = {
        id: "Sending",
        message: this.message,
        to: this.selectedFriend.id,
        index: this.selectedMessages.length,
        all_index: this.messages.length,
        created: moment().format("HH:mm A"),
        seen: false,
        type: "s",
      };

      this.socket.emit("send_message", msg);
      this.messages.push(msg);
      if (msg.to == this.selectedFriend.id) {
        this.selectedMessages.push(msg);
      }
      this.message = "";
      var container = this.$refs["cont"];
      container.scrollTop = container.scrollHeight;
    },
    checkFriend() {
      let token = this.$cookiz.get("auth_token");
      this.socket.emit("check_friend_phone", {
        token: token,
        phoneNumber: this.friendPhoneNumber,
      });
    },
    getIndexOfFriend(fr) {
      for (let f in this.friends) {
        if (this.friends[f].id == fr) {
          return f;
        }
      }
    },
    friendsInit() {
      this.friends.map((fr) => {
        this.friendsListInfo.push({
          id: fr.id,
          lastMessage: "Start messaging",
          created: null,
          unreads: 0,
        });
      });
    },
  },
  watch: {
    friends(nw, old) {
      if (old.length == 0 && nw.length != 0) {
        this.friendsInit();
      }
    },
    history(nw, old) {
      if (old.length == 0 && nw.length != 0) {
        nw.map((rmsg) => {
          if (rmsg.t == this.user.id) {
            console.log(rmsg);

            // Message to me from my friend
            var msg = {
              id: rmsg._id.$oid,
              message: rmsg.content,
              from: rmsg.f,
              seen: rmsg.seen,
              created: rmsg.created.$date,
              type: "r",
            };
          } else {
            // Message from me to my friend
            var msg = {
              id: rmsg._id.$oid,
              message: rmsg.content,
              to: rmsg.t,
              created: this.momentDate(rmsg.created.$date),
              seen: rmsg.seen,
              type: "s",
            };
          }
          this.messages.push(msg);
        });
        console.log(this.messages);
      }
    },
  },
  mounted() {
    this.socket.on("spam_detection", () => {
      alert("Spam detected");
    });
    this.socket.on("friend_seen", (id) => {
      this.selectedMessages.map((msg) => {
        if (msg.to == id) {
          msg.seen = true;
        }
      });
      this.messages.map((msg) => {
        if (msg.to == id) {
          msg.seen = true;
        }
      });
    });
    this.socket.on("double_check", (id) => {
      this.selectedMessages.map((msg) => {
        if (msg.id == id) {
          msg.seen = true;
        }
      });
      this.messages.map((msg) => {
        if (msg.id == id) {
          msg.seen = true;
        }
      });
    });
    this.socket.on("message_sent", (rmsg) => {
      this.selectedMessages[rmsg.index].id = rmsg.id;
      this.selectedMessages[rmsg.index].message = rmsg.message;
      this.messages[rmsg.all_index].id = rmsg.id;
      this.messages[rmsg.all_index].message = rmsg.message;
    });
    this.socket.on("receive_message", (rmsg) => {
      let msg = {
        id: rmsg.id,
        message: rmsg.message,
        from: rmsg.from,
        seen: false,
        created: rmsg.created,
        type: "r",
      };
      this.messages.push(msg);
      let index = this.getIndexOfFriend(rmsg.from);
      this.friendsListInfo[index].lastMessage = rmsg.message;
      this.friendsListInfo[index].created = rmsg.created;
      if (this.selectedFriend && this.selectedFriend.id == msg.from) {
        this.selectedMessages.push(msg);
        this.socket.emit("seen_message", msg);
      } else {
        this.friendsListInfo[index].unreads += 1;
      }
      var container = this.$refs["cont"];
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    });
    this.socket.on("get_friend_info", (friend_info) => {
      this.friendInfo = true;
      this.friendsExist = friend_info.status;
      if (this.friendsExist) {
        if (!friend_info.exist) {
          this.friendName = friend_info.user.name;
          this.friends.push(friend_info.user);
        } else {
          this.beforeAdded = true;
        }
      }
    });
  },
};
</script>

<style scoped lang="scss">
@import url("https://fonts.googleapis.com/css?family=Lato:400,700");
$font: "Lato", sans-serif, 20pt;

$primary: #79c7c5;
$secondary: #a1e2d9;
$white: #f9fbff;
$dark: #777777;
.in {
  background: #f5f5f5;
  max-width: 50%;
  color: black !important;
}
.out {
  width: 100%;
  background: transparent;
}
.html {
  display: grid;
  min-height: 100%;
}

.body {
  display: grid;
  background: linear-gradient(to bottom left, $primary 40%, $white 100%);
  font-family: $font;
}

.container {
  position: relative;
  margin: 1% auto;
  width: 1080px;
  height: 900px;
}

.messages {
  position: absolute;
  background: $white;
  opacity: 0.5;
  width: 30%;
  height: 70%;
  top: 2.5%;
  left: 5%;
  border-radius: 10px 0 0 10px;
  box-shadow: -5px 5px 10px rgba($dark, 0.5);
}

/*chat messages */
.people {
  position: absolute;
  list-style-type: none;
  width: 30.2%;
  left: -10px;
  top: 24.7%;
  line-height: 0.7em;
  .title {
    text-transform: uppercase;
    font-size: 0.7em;
    margin-left: 14px;
    letter-spacing: 1px;
    color: $dark;
  }
  .time {
    font-size: 0.3em;
    color: $dark;
    position: absolute;
    right: 10px;
    margin-top: 2px;
  }
  .preview {
    color: $primary;
    margin-left: 14px;
    font-size: 0.5em;
  }
}

.person {
  padding: 12px 0 12px 12px;
  border-bottom: 1px solid $primary;
  cursor: pointer;
  background: #f9fbff4a;
  &:hover {
    background: $white;
    transition: all 0.3s ease-in-out;
  }
}

.focus {
  background: $white;
  margin-left: 1px;
}

.profile {
  position: absolute;
  left: 16%;
  top: 7%;
}

.name2 {
  position: absolute;
  top: 50px;
  left: 2px;
  text-transform: uppercase;
  color: $primary;
  font-size: 0.8em;
  letter-spacing: 2px;
  font-weight: 500;
}
.email {
  color: $white;
  font-size: 1em;
  margin-left: -30px;
  margin-top: 2px;
}

.chatbox {
  position: absolute;
  left: 35%;
  height: 75%;
  width: 60%;
  background: white;
  border-radius: 10px;
  box-shadow: 5px 5px 15px rgba($dark, 0.5);
}
.chatbox-disabled {
  background: #b6b6b668;
  position: absolute;
  left: 35%;
  height: 75%;
  width: 60%;
  border-radius: 10px;
  box-shadow: 5px 5px 15px rgba($dark, 0.5);
}

.top-bar {
  width: 100%;
  height: 60px;
  background: $white;
  border-radius: 10px 10px 0 0;
}

.avatar {
  width: 35px;
  height: 35px;
  background: linear-gradient(to bottom left, $primary 20%, $secondary 100%);
  border-radius: 50%;
  position: absolute;
  top: 11px;
  left: 15px;
  p {
    color: $white;
    margin: 7px 12px;
  }
}

.name {
  position: absolute;
  top: 22px;
  text-transform: uppercase;
  color: $dark;
  font-size: 0.8em;
  letter-spacing: 2px;
  font-weight: 500;
  left: 60px;
}

.menu {
  position: absolute;
  right: 10px;
  top: 20px;
  width: 10px;
  height: 20px;
  cursor: pointer;
  &:hover {
    transform: scale(1.1);
    transition: all 0.3s ease-in;
  }
}

.icons {
  position: absolute;
  color: $secondary;
  padding: 10px;
  top: 5px;
  right: 21px;
  cursor: pointer;
  .fas {
    padding: 5px;
    opacity: 0.8;
    &:hover {
      transform: scale(1.1);
      transition: all 0.3s ease-in;
    }
  }
}

.dots {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: $primary;
  box-shadow: 0px 7px 0px $primary, 0px 14px 0px $primary;
}

.middle {
  position: absolute;
  overflow: scroll;
  background: $white;
  width: 100%;
  opacity: 0.85;
  bottom: 60px;
  height: 80%;
  padding: 60px;
  padding-right: 5px;
  padding-left: 5px;
}

.incoming {
  position: absolute;
  width: 50%;
  height: 100%;
  padding: 20px;
  .bubble {
    background: lighten($dark, 23%);
  }
}

.typing {
  position: absolute;
  top: 67%;
  left: 20px;
  .bubble {
    background: lighten($dark, 45%);
    padding: 8px 13px 9px 13px;
  }
}

.ellipsis {
  width: 5px;
  height: 5px;
  display: inline-block;
  background: lighten($dark, 25%);
  border-radius: 50%;
  animation: bounce 1.3s linear infinite;
}

.one {
  animation-delay: 0.6s;
}
.two {
  animation-delay: 0.5s;
}
.three {
  animation-delay: 0.8s;
}

.bubble {
  position: relative;
  display: inline-block;
  margin-bottom: 5px;
  color: $white;
  font-size: 0.7em;
  padding: 10px 10px 10px 12px;
  border-radius: 20px;
}

.lower {
  margin-top: 45px;
}

.outgoing {
  position: absolute;
  padding: 20px;
  right: 0;
  top: 15%;
  width: 50%;
  height: 100%;
  .bubble {
    background: $primary;
    float: right;
  }
}

.bottom-bar {
  position: absolute;
  width: 100%;
  height: 55px;
  bottom: 0;
  background: $white;
  border-radius: 0 0 10px 10px;
}

.left {
  left: 0px;
}

input {
  padding: 7px;
  width: 74%;
  left: 5%;
  position: absolute;
  border: 0;
  top: 13px;
  background: $white;
  color: $primary;
}

input::placeholder {
  color: $secondary;
}

input:focus {
  color: $dark;
  outline: 0;
}

button {
  position: absolute;
  border: 0;
  font-size: 1em;
  color: $secondary;
  top: 19px;
  opacity: 0.8;
  right: 17px;
  cursor: pointer;
  outline: 0;
  &:hover {
    transform: scale(1.1);
    transition: all 0.3s ease-in-out;
    color: $primary;
  }
}

footer {
  position: absolute;
  bottom: 0;
  right: 0;
  text-align: center;
  font-size: 0.7em;
  padding: 10px;
  p {
    color: $primary;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  a {
    color: $white;
    text-decoration: none;
    &:hover {
      color: $secondary;
    }
  }
}

@keyframes bounce {
  30% {
    transform: translateY(-2px);
  }
  60% {
    transform: translateY(0px);
  }
  80% {
    transform: translateY(2px);
  }
  100% {
    transform: translateY(0px);
    opacity: 0.5;
  }
}
</style>
