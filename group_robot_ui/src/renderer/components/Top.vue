<template>
  <div class="top-bar" v-show="show">
        <a><div @click='go_back' class='back ctrl-button'>
        <Icon type="arrow-left-a" size='30'></Icon><h4>后退</h4>
        </div></a>
        <a><div @click='go_forward' class='forward ctrl-button'>
        <Icon type="arrow-right-a" size='30'></Icon><h4>前进</h4>
        </div></a>
        <Menu mode="horizontal" theme="dark" @on-select='select'>
            <div class="layout-nav">
                <MenuItem name="login">
                    <Icon type="ios-navigate"></Icon>
                    登录
                </MenuItem>
                <MenuItem name="info">
                    <Icon type="ios-keypad"></Icon>
                    统计
                </MenuItem>
                <MenuItem name="group">
                    <Icon type="ios-analytics"></Icon>
                    管理
                </MenuItem>
            </div>
        </Menu>
    </div>
</template>

<script>
export default {
  computed: {
    show () {
      return this.$store.state.main.login.status == 2
    }
  },
  methods: {
    go_fresh: function () {
      window.location.reload()
    },
    go_exit: function () {
    },
    go_back: function () {
      this.$router.back()
    },
    go_forward: function () {
      this.$router.forward()
    },
    select: function (name) {
      if (this.$router.currentRoute.fullPath !== `/${name}/`) {
        this.$router.push(`/${name}/`)
      }
    }
  }
}
</script>

<style>
.top-bar {
    min-height: 60px;
    background-color: #495060;
}

.layout-nav{
    width: 270px;
    margin: 0 auto;
}

.ctrl-button{
    position: absolute;
    top: 5px;
    color: white;
    z-index: 999;
}

.fresh{
    right: 60px;
}
.exit{
    right: 13px;
}
.back{
    left: 13px;
}
.forward{
    right: 13px;
}
</style>
