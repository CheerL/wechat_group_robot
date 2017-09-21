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
    },
    mounted() {
      this.get_login_status()
      this.timer = setInterval(
        this.get_login_status,
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
