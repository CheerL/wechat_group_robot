<template>
  <div class="member_info" @click='handleClick'>
    <Avatar v-if='icon' class='member_avatar' :icon='icon' size="large" shape="square"/>
    <Badge v-else :dot='count'>
    <Avatar class='member_avatar' :src='member.pic_path' size="large" shape="square"/>
    </Badge>
    <div class='member_name'>
        {{name}}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    member: Object,
    icon: String,
    status: Number
  },
  data: function () {
    return {
      name: this.member.name.length <= 8 ? this.member.name : this.member.name.slice(0, 7) + '...',
      count: false
    }
  },
  methods: {
    handleClick (event) {
      if (this.status !== 0) {
        this.count = !this.count
        this.$emit('click', event, this.member)
      }
    }
  }
}
</script>

<style>
.member_info {
    width: 50px;
    height: 70px;
    float: left;
    margin: 5px;
}
.member_name {
    text-align: center
}
.member_avatar {
    left: 5px;
}
</style>
