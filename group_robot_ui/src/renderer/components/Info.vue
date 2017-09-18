<template>
    <div class='info'>
        <Collapse :value="['1', '2', '3']" style='borderRadius: 10px'>
            <Panel name="1">
                信息  
                <Row slot="content">
                    <img class="info_img" :src="pic_src">
                    <div class='info_user'>
                        <h1 style='margin: 14px'>{{name}}</h1>
                        <div class='info_item'>所在群组数：{{groups_num}}</div>
                    </div>
                </Row>
            </Panel>
            <Panel name="2">
                状态
                <div slot="content">
                    <div class='info_item'>转发开关：
                        <i-switch size="large" :value="trans_status" @on-change='change'>
                            <span slot="open">运行</span>
                            <span slot="close">停止</span>
                        </i-switch>
                    </div>
                    <div v-if='trans_status' class='info_item'>已开启转发群：
                        <Tag
                            v-for='(group, index) in trans_groups'
                            style='margin-right: 10px'
                            :key='index'
                            :color='get_type(index)'
                        >
                            {{group.name}}
                        </Tag>
                    </div>
                    <div v-if='trans_status' class='info_item'>
                        <p style="float: left">收集延时：</p>
                        <Input size='small' v-model="time.receive_delay" style='width: 50px'>
                        </Input>秒
                    </div>
                    <div v-if='trans_status' class='info_item'>
                        <p style="float: left">图文间隔：</p>
                        <Input size='small' v-model="time.msg_gap_low" style='width: 50px'>
                        </Input>秒
                        -
                        <Input size='small' v-model='time.msg_gap_up' style='width: 50px'>
                        </Input>秒
                    </div>
                    <div v-if='trans_status' class='info_item'>
                        <p style="float: left">群间隔：</p>
                        <Input size='small' v-model="time.group_gap_low" style='width: 50px'>
                        </Input>秒
                        -
                        <Input size='small' v-model="time.group_gap_up" style='width: 50px'>
                        </Input>秒
                    </div>
                    <div v-if='trans_status' class='info_item'>
                        <p style="float: left">休息：发</p>
                        <Input size='small' v-model="time.rest_msg_num" style='width: 50px'>
                        </Input>个图文休息
                        <Input size='small' v-model="time.rest_time" style='width: 50px'>
                        </Input>秒
                    </div>
                    <Button v-if='trans_status' class='info_item' @click="change_time">确认修改时间</Button>
                </div>
            </Panel>
            <Panel name="3">
                统计
                <div slot="content">
                <div class='info_item'>转发次数：{{trans_time}}</div>
                <div class='info_item'>转发文字消息数：{{trans_text}}</div>
                <div class='info_item'>转发图片消息数：{{trans_img}}</div>
                <div class='info_item'>拦截广告数：{{reject_time}}</div>
                </div>
            </Panel>
        </Collapse>
    </div>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'
import qs from 'qs'
const int_check = function (obj) {
    for (let i in obj) {
        if (!Number.isInteger(obj[i]) && !parseInt(obj[i]) && obj[i] != 0 && obj[i] != '0') {
            return false
        }
        else {
            obj[i] = parseInt(obj[i])
        }
    }
    return true
}

export default {
  name: 'info',
  data: function () {
    window.that = this
    return {
      type_list: [
        'blue',
        'green',
        'red',
        'yellow'
      ],
      state: that.$store.state.main,
      time: {
        receive_delay: that.$store.state.main.info.time.receive_delay,
        msg_gap_low: that.$store.state.main.info.time.msg_gap_low,
        msg_gap_up: that.$store.state.main.info.time.msg_gap_up,
        group_gap_low: that.$store.state.main.info.time.group_gap_low,
        group_gap_up: that.$store.state.main.info.time.group_gap_up,
        rest_msg_num: that.$store.state.main.info.time.rest_msg_num,
        rest_time: that.$store.state.main.info.time.rest_time
      }
    }
  },
  computed: {
    trans_status: () => {
      return that.state.trans_status
    },
    pic_src: () => {
        return that.state.info.pic_src
    },
    name: () => {
        return that.state.info.name
    },
    groups_num: () => {
        return that.state.info.groups_num
    },
    trans_groups: () => {
        return that.state.info.trans_groups
    },
    trans_time: () => {
        return that.state.info.trans_time
    },
    trans_text: () => {
        return that.state.info.trans_text
    },
    trans_img: () => {
        return that.state.info.trans_img
    },
    reject_time: () => {
        return that.state.info.reject_time
    },
    _time: () => {
        return that.state.info.time
    }
  },
  methods: {
    ...mapMutations([
      'change_trans_status'
    ]),
    ...mapActions([
      'get_robot_info'
    ]),
    get_type: index => {
      return that.type_list[index % 4]
    },
    change: val => {
      that.$http.post(
        `${that.state.host}/api/trans/`,
        qs.stringify({ trans_status: val })
      ).then(msg => {
        if (msg.data.res) {
          that.change_trans_status(val)
        }
      })
    },
    change_time: () => {
        if (
            int_check(that.time) &&
            parseInt(that.time.msg_gap_low) <= parseInt(that.time.msg_gap_up) &&
            parseInt(that.time.group_gap_low) <= parseInt(that.time.group_gap_up)
        ){
            that.$http.post(
                `${that.state.host}/api/time/`,
                qs.stringify({ time: JSON.stringify(that.time) })
                ).then(msg => {
                    if (msg.data.res) {
                        that.$Modal.info({
                            content: '修改成功'
                        })
                    }
                    else {
                        that.$Modal.info({
                            content: '修改失败'
                        })
                    }
                })
        }
        else {
            that.$Modal.info({
                content: '请确认时间下限小于上限，且输入的都是数字'
            })
        }
    }
  },
  mounted () {
    that.get_robot_info()
  },
  watch: {
      _time: val => {
          if (val != that.time) {
              that.time = val
          }
      }
  }
}
</script>

<style>
.info {
    padding: 15px;
}
.info_img {
    float: left;
    height: 100px;
    width: 100px;
    margin: 10px 50px;
}
.info_item {
    margin: 1em;
    line-height: 2em;
}
.info_user {
    float: left;
    position: relative;
}
</style>
