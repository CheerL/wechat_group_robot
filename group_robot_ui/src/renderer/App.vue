<template>
  <div id="app">
    <Top></Top>
    <router-view></router-view>
  </div>
</template>

<script>
  import Top from '@/components/Top'
  import { mapActions } from 'vuex'
  export default {
    name: 'ui',
    components: { Top },
    methods: {
      ...mapActions([
        'get_login_status',
        'get_robot_info',
        'get_group_list'
      ]),
      auto_update() {
        this.get_login_status()
      }
    },
    mounted() {
      this.auto_update()
      this.timer = setInterval(
        this.auto_update,
        30000
      )
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  }
</script>

<style>
  body {
    margin: 0;
    font-size: 12px;
    background-color: #eeeeee;
  }
</style>
