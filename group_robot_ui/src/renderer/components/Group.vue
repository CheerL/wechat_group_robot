<template>
  <Row class='group-box' type="flex" justify="center">
    <Col span="6" style='paddingRight: 8px'>
      <Menu
        ref='menu'
        class='group_list'
        @on-select="select"
        theme="light"
        width='auto'
        :active-name='menu_active'
      >
      <MenuGroup title="所有已加群">
        <Menu-item
          v-for='(group, index) in group_list'
          :key='index'
          :name='group.puid'
        >
          {{group.name}}
        </Menu-item>
      </MenuGroup>
      </Menu>
    </Col>
    <Col span='18' v-if='loading == 1' class="group-main">
        <Spin fix>
          <div>加载中...</div>
        </Spin>
    </Col>
    <Col span='18' v-else-if='loading == 2' class="group-main main">
        <h1 class='group-tip' @click='get_group({puid: menu_active, force: true})'>
          加载失败, 请点<b>此处</b>重试
        </h1>
    </Col>
    <Col span='18' v-else-if='loading == 0 && group_detail' class="group-main">
      <Row>
        <Col span='8'>
        <img class='group_img' :src="pic_src">
        </Col>
        <Col span='16'>
        <div class='group_info'>
            <h1 style='margin: 14px'>{{group_name}}</h1>
            <Row>
              <Col span='12'>
                <div class='group_item'>群人数：{{people_num}}</div>
              </Col>
              <Col span='12'>
                <Button style='float: right':disabled='sub_rule_edit || rule_edit' @click='rule_read'>
                  导入规则模板
                </Button>
              </Col>
            </Row>
            <Row>
              <Col span='12'>
                <div class='group_item'>群转发开关：
                  <i-switch :value='is_trans' @on-change='switch_group_trans' :disabled='!trans_status'>
                    <span slot="open">开</span>
                    <span slot="close">关</span>
                  </i-switch>
                </div>
              </Col>
              <Col span='12'>
                <Button style='float: right':disabled='sub_rule_edit || rule_edit' @click='rule_write'>
                  导出规则模板
                </Button>
              </Col>
            </Row>
          </div>
        </Col>
      </Row>
      <Row>
        <Collapse v-model="active">
          <!-- <Panel name='1'>
            <div class='pannel-head'>
            群成员管理
            </div>
            <div slot='content' class='group_member'>
              <Member
                v-for='(member, index) in group_member_list'
                :key='index'
                :member='member'
                :status='member_ctrl_status'
                @click='member_ctrl(member)'
              >
              </Member>
              <Member
                :member="{name:'添加成员'}"
                :icon='"plus-round"'
                @click='member_add'
              >
              </Member>
              <Member
                v-if="is_owner"
                :member="{name:'删除成员'}"
                :icon='"minus-round"'
                @click='member_del'
              >
              </Member>
              <Member
                v-if='member_ctrl_status'
                :member="{name:'完成'}"
                :icon='"checkmark-round"'
                @click='member_back'
              >
              </Member>
            </div>
          </Panel> -->
          <Panel name='2'>
            <div class='pannel-head'>
              转发目标管理
              <Button
                  class='pannel-head-buttom'
                  v-if='!target_edit'
                  size='small'
                  icon='edit'
                  @click.stop='target_edit=true'
              >
                  编辑
              </Button>
              <Button
                v-else
                class='pannel-head-buttom'
                size='small'
                icon='checkmark'
                @click.stop='target_edit_finish'
              >
                  完成
              </Button>
            </div>
            <Target slot="content" :targetGroup='target_group' :edit='target_edit'></Target>
          </Panel>
          <Panel name='4'>
            <div class='pannel-head'>
              白名单设置
              <Button
                  class='pannel-head-buttom'
                  v-if='!white_edit'
                  size='small'
                  icon='edit'
                  @click.stop='white_edit=true'
              >
                  编辑
              </Button>
              <Button
                v-else
                class='pannel-head-buttom'
                size='small'
                icon='checkmark'
                @click.stop='white_edit_finish'
              >
                  完成
              </Button>
            </div>
            <White slot="content" :white='white' :edit='white_edit'></White>
          </Panel>
          <Panel name='3'>
            <div class='pannel-head'>
            规则管理
            <Button
                  class='pannel-head-buttom'
                  v-if='!rule_edit'
                  size='small'
                  icon='edit'
                  @click.stop='rule_edit=true'
              >
                  编辑
              </Button>
              <ButtonGroup
                v-else
                class='pannel-head-buttom'
              >
                <Button
                  size='small'
                  icon='plus'
                  @click.stop='add_rule'
                  :disabled='sub_rule_edit'
                >
                  添加
                </Button>
                <Button
                  size='small'
                  icon='checkmark'
                  @click.stop='rule_edit_finish'
                  :disabled='sub_rule_edit'
                >
                    完成
                </Button>
              </ButtonGroup>
              <div
                v-if='rule_edit'
                @click.stop="()=>{}"
                class='pannel-head-buttom'
                style='width: 200px; lineHeight: 24px'
              >
              <Select
                size='small'
                v-model="copy_rule_index"
                placeholder='下拉选择复制已有规则'
                @on-change='copy_rule'
                :disabled='sub_rule_edit'
              >
                <Option
                  v-for='(rule, index) in all_rules()'
                  :key='index'
                  :value="index"
                >
                  {{ `${rule.group}：${rule.keyword}` }}
                </Option>
              </Select>
              </div>
            </div>
            <div slot="content">
              <Rule
                :rules='rule_list'
                :edit='rule_edit'
                :Focus='focus'
                @on-edit='sub_rule_on_edit'
                @over-edit='sub_rule_over_edit'
              >
              </Rule>
            </div>
          </Panel>
        </Collapse>
      </Row>
    </Col>
    <Col span='18' v-else class="group-main main">
        <h1 class='group-tip'>请选择一个群</h1>
    </Col>
  </Row>
</template>

<script>
import Rule from '@/components/Group/Rule'
import Member from '@/components/Group/Member'
import Target from '@/components/Group/Target'
import White from '@/components/Group/White'
import { mapActions, mapMutations } from 'vuex'
import fs from 'fs'
const {dialog} = require('electron').remote

const detail_item = (detail, item) => {
  if (detail) {
    return detail[item]
  } else {
    return null
  }
}

export default {
  name: 'group',
  components: { Member, Rule, Target, White },
  data: function () {
    window.that = this
    return {
      state: that.$store.state.main,
      active: ['2', '3', '4'],
      out_rule: [],
      menu_active: null,
      member_ctrl_status: 0,
      target_edit: false,
      white_edit: false,
      sub_rule_edit: false,
      rule_edit: false,
      copy_rule_index: null,
      del_member_list: [],
      focus: null
    }
  },
  computed: {
    trans_status: () => {
      return that.state.trans_status
    },
    group_puid: () => {
      let puid = that.state.group_puid
      that.menu_active = puid
      return puid
    },
    group_list: () => {
      return that.state.group_list
    },
    white: () => {
      return detail_item(that.group_detail, 'white')
    },
    group_detail: () => {
      return that.state.groups_detail[that.group_puid]
    },
    group_member_list: () => {
      return detail_item(that.group_detail, 'group_member_list')
    },
    rule_list: () => {
      return detail_item(that.group_detail, 'rule_list')
    },
    target_group: () => {
      return detail_item(that.group_detail, 'target_group')
    },
    people_num: () => {
      return detail_item(that.group_detail, 'people_num')
    },
    group_name: () => {
      return detail_item(that.group_detail, 'group_name')
    },
    pic_src: () => {
      return detail_item(that.group_detail, 'pic_src')
    },
    is_owner: () => {
      return detail_item(that.group_detail, 'is_owner')
    },
    is_trans: () => {
      return detail_item(that.group_detail, 'is_trans')
    },
    loading: () => {
      return that.state.loading
    },
  },
  methods: {
    ...mapActions([
      'get_group_list',
      'get_robot_info',
      'get_group',
      'switch_group_trans',
      'set_target_group',
      'set_rule',
      'set_white',
      'del_member'
    ]),
    ...mapMutations([
      'change_loading'
    ]),
    leave: index => {
      that.rule_edit = false
      that.target_edit = false
      that.white_edit = false
      that.sub_rule_edit = false
      if (that.focus) {
        if (that.focus.keyword.length === 0) {
          for (let each in that.rule_list) {
            if (that.rule_list[each].edit) {
              that.rule_list.splice(each, 1)
              break
            }
          }
        }
        else {
          that.focus.edit = false
          that.focus = null
        }
      }
      that.get_group({puid: index})
      that.menu_active = index
    },
    select: index => {
      if (index !== that.group_puid) {
        if (that.rule_edit || that.target_edit || that.white_edit) {
        that.$Modal.confirm({
            content: '仍有修改尚未提交。是否确认离开',
            okText: '确认离开',
            cancelText: '留下',
            onOk: () => {that.leave(index)},
            onCancel: () => {
              that.$refs.menu.currentActiveName = that.menu_active
            }
          })
        }
        else{
          that.leave(index)
        }
      } else {
        that.get_group({puid: index, force: true})
        that.leave(index)
      }
    },
    member_ctrl: member => {
      that.del_member_list.push(member.puid)
    },
    member_add: () => {
      that.member_ctrl_status = 1
    },
    member_del: () => {
      that.member_ctrl_status = 2
    },
    member_back: () => {
      that.member_ctrl_status = 0
      if (that.del_member_list.length > 0) {
        that.del_member(that.del_member_list)
      }
    },
    del_rule: index => {
      let temp_list = that.rule_list
      temp_list.splice(index, 1)
      that.rule_list = temp_list
    },
    refresh_group_list: () => {
      that.get_group_list(true)
    },
    target_edit_finish: () => {
      that.target_edit = false
      that.set_target_group(that.target_group)
    },
    rule_edit_finish: () => {
      that.rule_edit = false
      that.set_rule(that.rule_list)
    },
    white_edit_finish: () => {
      that.white_edit = false
      that.set_white(that.white)
    },
    add_rule: () => {
      that.rule_list.push({
        keyword: '',
        include_words: [],
        reject_words: [],
        head: '',
        tail: '',
        success_report: '【@被收集者】 已收集到【关键词】消息，并收集到【收集的图片数量】张图片，稍后将为您转发',
        fail_report: '【@被收集者】 您发送的消息与【关键词】无关，也请不要包含【广告词】，此类消息不予转发，谢谢',
        result_report: '【@被收集者】 已为您成功发送【关键词】消息到【已发送群数量】个群，预计将会被【所有群人数】人看到',
        start_report: '【@被收集者】 开始接收【关键词】消息，请在【收集时长】秒内输入相关信息, 若意外触发，请发送[中止]停止收集',
        include_report: '【@被收集者】 您所发送的内容信息不全，【关键词】应至少包含【包含词】',
        index: new Date().getTime(),
        group: that.group_name,
        edit: true
      })
      that.sub_rule_edit = true
      that.focus = that.rule_list[that.rule_list.length - 1]
    },
    all_rules: () => {
      let all = []
      for (let each in that.state.groups_detail){
          each = that.state.groups_detail[each]
          all.push.apply(all, each.rule_list)
      }
      return all.concat(that.out_rule)
    },
    copy_rule: index => {
      let rule = that.all_rules()[index]
      that.rule_list.push({
        keyword: rule.keyword,
        include_words: rule.include_words,
        reject_words: rule.reject_words,
        head: rule.head,
        tail: rule.tail,
        success_report: rule.success_report,
        fail_report: rule.fail_report,
        result_report: rule.result_report,
        start_report: rule.start_report,
        include_report: rule.include_report,
        index: new Date().getTime(),
        group: that.group_name,
        edit: false
      })
    },
    sub_rule_on_edit: focus => {
      that.sub_rule_edit = true
      that.focus = focus
    },
    sub_rule_over_edit: focus => {
      that.sub_rule_edit = false
      that.focus = focus
    },
    rule_write: () => {
      let path = process.env.NODE_ENV === 'development' ?
        `${process.cwd()}\\build\\api\\src`:
        `${__dirname}\\..\\..\\..\\api\\src`
      dialog.showSaveDialog({
        title: '规则导出',
        defaultPath: path,
        filters: [{name:'*', extensions: ['json']}]
      }, file => {
        console.log(file)
        if (file === undefined){
          that.$Modal.warning({
            content: '你没有选择文件，导出取消'
          })
          return
        }
        let all = []
        for (let each in that.state.groups_detail){
            each = that.state.groups_detail[each]
            all.push.apply(all, each.rule_list)
        }
        fs.writeFile(file, JSON.stringify(all), (err) => {
            if(err){
                that.$Modal.info({
                  content: '规则模板导出失败，请重试'
                })
            }
            that.$Modal.info({
              content: '规则模板导出成功'
            })
        })
      })
    },
    rule_read: () => {
      let path = process.env.NODE_ENV === 'development' ?
        `${process.cwd()}\\build\\api\\src`:
        `${__dirname}\\..\\..\\..\\api\\src`
      dialog.showOpenDialog(
        {
          title: '规则导入',
          defaultPath: path,
          filters: [{name:'*', extensions: ['json']}]
        }, 
        file => {
          file = file[0]
          console.log(file)
          if (file === undefined){
            that.$Modal.warning({
              content: '你没有选择文件，导入取消'
            })
            return
          }
          fs.readFile(file, 'utf-8', (err, data) => {
              if(err){
                  that.$Modal.info({
                    content: '规则模板导入失败，请重试'
                  })
              }
              that.out_rule = JSON.parse(data)
              for (let each in that.out_rule) {
                that.out_rule[each].group = '模板'
              }
              that.$Modal.info({
                content: '规则模板导入成功'
              })
          })
        })
    }
  },
  mounted () {
    that.get_group_list()
    that.menu_active = that.group_puid
    that.$refs.menu.currentActiveName = that.menu_active
    that.get_robot_info()
  }
}
</script>

<style>
.main {
  text-align: center;
}
.group-tip {
  position: relative;
  top: 45%;
}
.group-box {
  max-width: 100vw;
  margin: 0;
  padding: 15px;
  border-radius: 10px;
}
.group-main {
  background-color: white;
  border-radius: 10px;
}
.pannel-head {
  position: relative;
  float: left;
  margin-right: 1em;
  width: 95%;
}

.pannel-head-buttom {
  position: relative;
  float: right;
  margin-top: 7px;
}

.group_list {
  height: calc(100vh - 90px);
  border-radius: 10px;
}

.no-overflow {
  overflow-y: visible;
  overflow-x: hidden;
}

.group_img {
    float: left;
    height: 100px;
    width: 100px;
    margin: 10px 50px;
}
.group_item {
    font-size: 14px;
    margin: 0.5em;
}
.group_info {
    width: 90%;
    float: left;
    position: relative;
}
</style>
