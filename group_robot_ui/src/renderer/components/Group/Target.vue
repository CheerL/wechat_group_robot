<template>
  <div class='target'>
    <div
        v-for="(group, index) in inner_target_group"
        :key="index"
        class='tag_item'
    >
        <Tag
            :closable='edit'
            :name="group.puid"
            @on-close="del(index)"
        >
            {{group.name}}
        </Tag>
    </div>
    <Select
        filterable
        v-if='edit'
        size='small'
        style="height: 24px; margin: 1px; width: auto;"
        placeholder='请选择（可输入搜索）'
        @on-change='add'
    >
        <Option v-for="(group, index) in select_list" :value="group.puid" :key="group.puid">{{ group.name }}</Option>
    </Select>
  </div>
</template>

<script>
export default {
  props: {
    targetGroup: Array,
    edit: Boolean
  },
  data: function () {
    window._target = this
    return {
      state: this.$store.state.main,
      new_item: null,
      inner_target_group: this.targetGroup
    }
  },
  computed: {
    group_list () {
      return this.state.group_list
    },
    select_list () {
      if (this.group_list && this.inner_target_group) {
        return this.group_list_minus(this.group_list, this.inner_target_group)
      } else {
        return []
      }
    }
  },
  methods: {
    add (puid) {
      if (puid !== '') {
        for (let group of this.group_list) {
          if (group.puid === puid) {
            this.inner_target_group.push(group)
            break
          }
        }
      }
    },
    del (index) {
      this.inner_target_group.splice(index, 1)
    },
    group_list_minus: (list1, list2) => {
      let result = []
      let obj = {}
      for (let each of list2) {
        obj[each.puid] = true
      }
      for (let each of list1) {
        if (!obj[each.puid]) {
          obj[each.puid] = true
          result.push(each)
        }
      }
      return result
    }
  },
  watch: {
    targetGroup(val) {
      this.inner_target_group = val
    }
  }
}
</script>

<style>
.tag_item {
    float: left;
    margin-bottom: 1em;
}
</style>
