<template>
    <div class="login">
        <img class="login_img" :src="pic_path">
        <div class="login_text">{{text}}</div>
        <Button class='login_button' type='ghost' @click='login_func' v-if='status==0'>登录</Button>
        <Button class='login_button' type="error" @click='logout_func' v-else-if='status==2'>退出</Button>
        <Modal v-model="tip" title='登录失败'>
          <p>登录失败，请重新登录</p>
          <p>若多次出现次提示，可能是账号被限制登录</p>
        </Modal>
    </div>
</template>

<script>
import io from 'socket.io-client'
import { mapActions, mapMutations } from 'vuex'

export default {
  name: 'login',
  data: function () {
    window.that = this
    return {
      state: that.$store.state.main,
      tip: false
    }
  },
  computed: {
    host: () => {
      return that.state.host
    },
    pic_path: () => {
      return that.state.login.pic_path
    },
    text: () => {
      return that.state.login.text
    },
    status: () => {
      return that.state.login.status
    }
  },
  methods: {
    ...mapMutations([
      'change_login'
    ]),
    ...mapActions([
      'get_login_status'
    ]),
    login_func: () => {
      that.new_socket()
      that.socket.emit('login')
    },
    logout_func: () => {
      that.new_socket()
      that.socket.emit('logout')
    },
    cancel_func: () => {
    },
    new_socket: () => {
      if (!that.socket) {
        that.socket = io.connect(that.host)
        that.socket.on('connect', () => {
          that.socket.emit('client-send', 'client connect')
        })
        that.socket.on('server-send', msg => {
          if (msg.style === 'login') {
            that.change_login(msg)
          } else if (msg.style === 'error') {
            that.tip = true
          }
        })
      }
    },
    close_socket: () => {
      if (that.socket) {
        that.socket.disconnect()
        that.socket = null
      }
    }
  },
  mounted () {
    this.get_login_status()
    this.new_socket()
  },
  beforeDestroy () {
    this.close_socket()
  },
  watch: {
    status: val => {
      if (val === 2) {
        that.close_socket()
      }
    }
  }
}
</script>

<style>
.login {
    position: relative;
    width: 250px;
    height: 335px;
    left: calc(50vw - 125px);
    top: calc(50vh - 197px);
    background-color: #f6f9f6;
    text-align: center;
    border-radius: 10px;
    box-shadow: 3px 3px 7px 3px rgba(0, 0, 0, .1), inset 2px 2px 2px rgba(255, 255, 255, .2);
}

.login_img {
    height: 235px;
    width: 235px;
    margin-top: 8px;
}

.login_text {
    margin: 0.5em 0 0 0;
    text-align: center;
}

.login_button {
    width: 6em;
    margin-top: 0.65em;
}
</style>
