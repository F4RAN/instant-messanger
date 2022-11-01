<template>
  <div id="app">
    hello
    <button type="" @click="test()">test</button>
  </div>
</template>

<script>
import SocketIO from './assets/socket.io.esm.min.js'

export default {
  name: 'App',
  data(){
    return{
      socket:''
    }
  },
  methods: {
    test(){
      this.socket.emit('message','test')
      console.log(this.socket)
    }
  },
  mounted() {
    this.socket = SocketIO('http://127.0.0.1:5000/',{
  reconnectionDelayMax: 10000,
  query: {
    "token": "very_strong_token2"
  }
})
    this.socket.on('accepted',() => {
      console.log('server accepted your connection')
    })
    this.socket.on('rejected',() => {
      console.error('server rejected your connection (auth failed)')
    })
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
