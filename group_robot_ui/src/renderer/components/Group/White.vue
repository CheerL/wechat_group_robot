<template>
  <div class='white'>
    <div
        v-for="(person, index) in inner_white"
        :key="index"
        class='tag_item'
    >
        <Tag
            :closable='edit'
            :name="person"
            @on-close="del(index)"
        >
            {{person}}
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
        <Option v-for="(person, index) in select_list" :value="person.name" :key="person.name">{{ person.name }}</Option>
    </Select>
  </div>
</template>

<script>
export default {
  props: {
    white: Array,
    edit: Boolean
  },
  data: function () {
    window._white = this
    return {
      state: this.$store.state.main,
      new_item: null,
      inner_white: this.white
    }
  },
  computed: {
    people_list () {
      return this.state.groups_detail[this.state.group_puid]['group_member_list']
    },
    select_list () {
        return this.member_list_minus(this.people_list, this.inner_white)
    }
  },
  methods: {
    add (name) {
      if (name !== '') {
        for (let person of this.people_list) {
          if (person.name === name) {
            this.inner_white.push(person.name)
            break
          }
        }
      }
    },
    del (index) {
      this.inner_white.splice(index, 1)
    },
    member_list_minus: (list1, list2) => {
      let result = []
      let obj = {}
      for (let each of list2) {
        obj[each] = true
      }
      for (let each of list1) {
        if (!obj[each.name]) {
          obj[each.name] = true
          result.push(each)
        }
      }
      return result
    }
  },
  watch: {
    white(val) {
      this.inner_white = val
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
