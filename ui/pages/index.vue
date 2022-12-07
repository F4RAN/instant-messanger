<template>
  <div>
    <Register
      @submit="
        form = $event;
        register();
      "
      v-if="!isRegistered"
    ></Register>
    <Chat
      :socket="socket"
      :user="user"
      :friends="friends"
      :history="history"
      v-else
    ></Chat>
  </div>
</template>
<script>
import SocketIO from "@/assets/socket.io.esm.min.js";

export default {
  data() {
    return {
      isRegistered: false,
      form: "",
      user: "",
      socket: "",
      token: "",
      friends: [],
      history: [],
    };
  },
  methods: {
    register() {
      console.log(this.form);
      this.socket.emit("register", this.form);
    },
  },
  mounted() {
    this.socket = SocketIO("http://127.0.0.1:5000/", {
      reconnectionDelayMax: 10000,
      query: {
        token: this.$cookiz.get("auth_token"),
      },
    });
    this.socket.on("accepted", (user) => {
      this.isRegistered = true;
      this.user = user;
      console.log("server accepted your connection");
    });
    this.socket.on("rejected", () => {
      this.isRegistered = false;
      console.error("server rejected your connection (auth failed)");
    });
    this.socket.on("get_token", (token) => {
      this.$cookiz.set("auth_token", token);
      this.token = token;
      this.socket.emit("get_init_data");
    });
    this.socket.emit("get_friends");
    this.socket.on("friends_list", (friends) => {
      this.friends = friends;
    });
    this.socket.emit("get_messages_history");
    this.socket.on("messages_history", (msgs) => {
      this.history = msgs;
    });
  },
};
</script>
