<template>
  <div>
    <div class="register">
      <div class="field" v-if="field == 'phone'">
        <input
          @input="
            phoneNumber.length < 10
              ? (phoneNumber = $event.target.value)
              : (phoneNumber = $event.target.value) && (field = 'name')
          "
          id="register"
          maxlength="11"
          type="text"
        /><label for="register"><span>(IR) +98</span></label
        ><button>OK</button>
      </div>
      <div class="field" v-if="field == 'name'">
        <input v-model="name" maxlength="11" type="text" /><label for="name"
          ><span>Name</span></label
        ><button :class="name.length > 3 ? 'active' : ''" @click="register()">OK</button>
      </div>
    </div>
  </div>
</template>

<script>
import SocketIO from "@/assets/socket.io.esm.min.js";

export default {
  data() {
    return {
      field: "phone",
      phoneNumber: "",
      name: "",
    };
  },
  methods: {
    register() {
      this.$emit("submit", { phoneNumber: this.phoneNumber, name: this.name });
    },
  },
};
</script>
<style scoped lang="scss">
// Inspired by Derek Torsani :
// https://dribbble.com/shots/2359423-Daily-UI-026-Subscribe

@mixin size($width: null, $height: $width) {
  width: $width;
  height: $height;
}

%reset {
  margin: 0;
  padding: 0;
}

html,
body {
  @include size($width: 100%);
  @extend %reset;
  overflow: hidden;
}

*,
*:before,
*:after {
  box-sizing: border-box;
  outline: none;
}

body {
  background: linear-gradient(to bottom, #639edb, #0668cf) no-repeat;
  font-family: "Arimo", sans-serif;
  background-size: 100%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

p {
  text-align: center;
  color: #ffffff;
  font-size: 13px;
}

a {
  &:hover,
  &:visited,
  &:hover,
  &:link {
    color: rgba(255, 255, 255, 0.6);
  }
}

.register {
  margin: 0 auto 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.field {
  width: 385px;
  height: 70px;
  position: relative;
  input {
    width: 100%;
    border-radius: 6px;
    height: 70px;
    border: 0;
    padding: 10px;
    padding: 20px 0 0 16px;
    font-size: 0;
    background: #1566bb;
    transition: background 0.3s ease;
    color: #ffffff;

    &:focus {
      background: #065cb7;
      font-size: 23px;

      &::selection {
        background: rgba(188, 232, 255, 0.5);
      }
    }
    &.active {
      background: #065cb7;
      font-size: 23px;
    }
  }
  input,
  button {
    position: absolute;
    height: 70px;
  }
  button {
    background: rgba(0, 0, 0, 0.3);
    right: 0;
    border: 0;
    width: 115px;
    border-radius: 6px;
    font-size: 22px;
    cursor: pointer;
    transition: width 0.3s ease, background 0.3s ease, opacity 0.3s ease;
    opacity: 0;
    color: #065cb7;
    text-transform: uppercae;
    pointer-events: none;
    &.active {
      color: #ffffff;
      background: #639edb;
      opacity: 1;
      pointer-events: auto;
      &:hover {
        background: #5e99d6;
      }
    }
    &.full {
      width: 100%;
    }
  }
  input:focus + label {
    font-size: 19px;
    transform: translate(16px, 11px);
    color: rgba(255, 255, 255, 0.7);
  }
  label {
    position: absolute;
    color: rgba(255, 255, 255, 1);
    transform: translate(16px, 20px);
    transition: transform 0.3s ease, font-size 0.3s ease, color 0.3s 0.1s ease;
    font-size: 28px;
    &.active {
      font-size: 19px;
      transform: translate(16px, 11px);
      color: rgba(255, 255, 255, 0.7);
    }
  }
  input:focus + label + button {
    opacity: 1;
  }
}
</style>
