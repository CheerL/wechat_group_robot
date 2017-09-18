<template>
<div>
  <Card 
    class='card'
    v-for='(rule, index) in inner_rules'
    :key='index'
    :rule='rule'
    @del-rule='del_rule(index)'
  >
    <div slot="title" class='card_title'>
        <p v-if='!rule.edit' style='float:left; width: 250px'>关键词：{{rule.keyword}}</p>
        <div v-else style="float:left; width: 250px">
            <p style="float: left; width: auto">关键词：</p>
            <Input v-model="rule.keyword" style='width: 180px;' size='small'>
            </Input>
        </div>
        <Button
            v-if='!rule.edit && edit'
            size='small'
            style='float: right'
            icon='edit'
            @click.stop='edit_rule(rule)'
        >
            编辑
        </Button>
        <ButtonGroup v-else-if="rule.edit && edit" style='float: right'>
        <Button
            size='small'
            icon='close'
            @click='del_rule(index)'
        >
            删除
        </Button>
        <Button
            size='small'
            icon='checkmark'
            @click='edit_finish(rule)'
        >
            完成
        </Button>
        </ButtonGroup>
    </div>
    
    <div class='inner_rule_item'>
        <b style='float:left'>包含词：</b>
        <div
            v-for="(item, _index) in rule.include_words"
            :key="_index"
            class='rule_tag_item'
        >
            <Input
                v-if='item === ""'
                v-model="include_new_word"
                placeholder="请输入, 回车键确认"
                style="width: 120px; height: 24px; margin: 1px"
                size='small'
                @on-enter="include_new(rule, _index)"
            >
            </Input>
            <Tag
                v-else
                :closable='rule.edit'
                :name="item"
                @on-close="include_del(rule, _index)"
            >
                {{item}}
            </Tag>
        </div>
        <Button
            v-if='rule.edit && !include_new_status'
            icon="ios-plus-empty"
            type="dashed"
            size="small"
            style="height: 24px; margin: 1px"
            @click="include_add(rule)"
        >
            添加包含词
        </Button>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>限制词：</b>
        <div
            v-for="(item, _index) in rule.reject_words"
            :key="_index"
            class='rule_tag_item'
        >
            <Input
                v-if='item === ""'
                v-model="reject_new_word"
                placeholder="请输入, 回车键确认"
                style="width: 120px; height: 24px; margin: 1px"
                size='small'
                @on-enter="reject_new(rule, _index)"
            >
            </Input>
            <Tag
                v-else
                :closable='rule.edit'
                :name="item"
                @on-close="reject_del(rule, _index)"
            >
                {{item}}
            </Tag>
        </div>
        <Button
            v-if='rule.edit && !reject_new_status'
            icon="ios-plus-empty"
            type="dashed"
            size="small"
            style="height: 24px; margin: 1px"
            @click="reject_add(rule)"
        >
            添加限制词
        </Button>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>消息头：</b>
        <div v-if='!rule.edit'>{{rule.head}}</div>
        <Input v-else v-model="rule.head" style='width: 70%' size='small'></Input>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>消息尾：</b>
        <div v-if='!rule.edit'>{{rule.tail}}</div>
        <Input v-else v-model="rule.tail" style='width: 70%' size='small'></Input>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>开始返回语句：</b>
        <div v-if='!rule.edit'>{{rule.start_report}}</div>
        <Input v-else v-model="rule.start_report" style='width: 70%' size='small'></Input>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>成功返回语句：</b>
        <div v-if='!rule.edit'>{{rule.success_report}}</div>
        <Input v-else v-model="rule.success_report" style='width: 70%' size='small'></Input>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>失败返回语句：</b>
        <div v-if='!rule.edit'>{{rule.fail_report}}</div>
        <Input v-else v-model="rule.fail_report" style='width: 70%' size='small'></Input>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>缺失返回语句：</b>
        <div v-if='!rule.edit'>{{rule.include_report}}</div>
        <Input v-else v-model="rule.include_report" style='width: 70%' size='small'></Input>
    </div>
    <div class='inner_rule_item'>
        <b style='float:left'>结果返回语句：</b>
        <div v-if='!rule.edit'>{{rule.result_report}}</div>
        <Input v-else v-model="rule.result_report" style='width: 70%' size='small'></Input>
    </div>
  </Card>
  <Modal
    v-model='have_error'
    @on-ok='clear_error'
    @on-cancel='clear_error'
    title='规则错误'
    :mask-closable="false"
    :closable="false"
    >
      <p v-for='err in error' :key='err'>{{err}}</p>
  </Modal>
</div>
</template>

<script>

String.prototype.contain = function(list) {
    for (let substr of list) {
        if (! new RegExp(substr).test(this)) {
            return false
        }
    }
    return true
}

export default {
  props: {
    rules: Array,
    edit: Boolean,
    Focus: Object
  },
  data: function () {
    window._rule = this
    return {
      focus: this.Focus,
      inner_rules: this.rules,
      include_new_status: false,
      reject_new_status: false,
      reject_new_word: '',
      include_new_word: '',
      have_error: false,
      error: []
    }
  },
  methods: {
    clear_error () {
        this.error = []
        this.have_error = false
    },
    end_process () {
      if (this.focus) {
        this.include_new(this.focus, this.focus.include_words.length - 1)
        this.reject_new(this.focus, this.focus.reject_words.length - 1)
        if (this.focus.keyword.length === 0) {
            this.error.push('必须设定关键词')
        }
        if (!this.focus.start_report.contain(['【@被收集者】', '【关键词】', '【收集时长】'])) {
            this.error.push('开始返回语句必须包含：“【@被收集者】”，“【关键词】”，“【收集时长】”')
        }
        if (!this.focus.success_report.contain(['【@被收集者】', '【关键词】', '【收集的图片数量】'])) {
            this.error.push('成功返回语句必须包含：“【@被收集者】”，“【关键词】”，“【收集的图片数量】”')
        }
        if (!this.focus.fail_report.contain(['【@被收集者】', '【关键词】', '【广告词】'])) {
            this.error.push('失败返回语句必须包含：“【@被收集者】”，“【关键词】”，“【广告词】”')
        }
        if (!this.focus.include_report.contain(['【@被收集者】', '【关键词】', '【包含词】'])) {
            this.error.push('缺失返回语句必须包含：“【@被收集者】”，“【关键词】”，“【包含词】”')
        }
        if (!this.focus.result_report.contain(['【@被收集者】', '【关键词】', '【已发送群数量】', '【所有群人数】'])) {
            this.error.push('结果返回语句必须包含：“【@被收集者】”，“【关键词】”，“【已发送群数量】”，“【所有群人数】”')
        }
        if (this.error.length > 0) {
            this.have_error = true
        }
        else {
            this.focus.edit = false
            this.focus = null
        }
      }
    },
    edit_rule (rule) {
      this.end_process()
      if (!this.focus) {
        rule.edit = true
        this.focus = rule
        this.$emit('on-edit', this.focus)
      }
    },
    include_add (rule) {
      rule.include_words.push('')
      this.include_new_status = true
    },
    include_del (rule, index) {
      rule.include_words.splice(index, 1)
    },
    include_new (rule, index) {
        if (rule.include_words[index] === '') {
            if (this.include_new_word !== '') {
                rule.include_words[index] = this.include_new_word
                this.include_new_word = ''
            }
            else {
                rule.include_words.splice(index, 1)
            }
        }
        this.include_new_status = false
    },
    reject_add (rule) {
      rule.reject_words.push('')
      this.reject_new_status = true
    },
    reject_del (rule, index) {
      rule.reject_words.splice(index, 1)
    },
    reject_new (rule, index) {
        if (rule.reject_words[index] === '') {
            if (this.reject_new_word !== '') {
                rule.reject_words[index] = this.reject_new_word
                this.reject_new_word = ''
            }
            else {
                rule.reject_words.splice(index, 1)
            }
        }
        this.reject_new_status = false
    },
    edit_finish (rule) {
      this.end_process()
      if (!this.focus) {
        this.$emit('over-edit', this.focu)
      }
    },
    del_rule (index) {
      this.inner_rules.splice(index, 1)
      this.$emit('over-edit', this.focu)
    },
    closing () {
        console.log('close')
        for (let i in this.inner_rules) {
            let rule = this.inner_rules[i]
            if (rule.keyword.length === 0) {
                console.log(rule)
                this.inner_rules.splice(i, 1)
            }
        }
    }
  },
  watch: {
    rules (val) {
        this.inner_rules = val
    },
    Focus (val) {
        if (val !== this.focus) {
            this.focus = val
        }
    }
  }
}
</script>

<style>
.card {
    margin-bottom: 10px;
}
.card_title {
    min-height: 20px;
}
.inner_rule_item {
    font-size: 14px;
    margin: 1em;
    min-height: 26px;
}
.rule_tag_item {
    float: left;
    min-height: 26px;
}
</style>
