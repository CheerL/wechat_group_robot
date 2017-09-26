import axios from 'axios'
import qs from 'qs'
import router from '@/router'

const state = {
    host: process.env.NODE_ENV === 'production' ? 'http://localhost:9777' : 'http://localhost:9777',
    login: {
        text: '请点击登录按钮',
        pic_path: '',
        status: 0
    },
    trans_status: false,
    group_list: [],
    update_time: {
        group_list: 0
    },
    groups_detail: {},
    group_puid: null,
    loading: false,
    info: {
        name: '',
        pic_src: '',
        time: {
            receive_delay: 30,
            msg_gap_low: 100,
            msg_gap_up: 300,
            group_gap_low: 100,
            group_gap_up: 300,
            rest_msg_num: 10,
            rest_time: 5
        },
        groups_num: 0,
        trans_time: 0,
        trans_text: 0,
        trans_img: 0,
        trans_groups: [],
        reject_time: 0
    }
}

const mutations = {
    change_login: (state, val) => {
        state.login.text = val.text
        state.login.pic_path = val.pic_path
        state.login.status = val.status
    },
    change_loading: (state, val) => {
        state.loading = val
    },
    change_trans_status: (state, val) => {
        state.trans_status = val
    },
    change_group_list: (state, val) => {
        state.group_list = val
    },
    change_update_time: (state, playload) => {
        state.update_time[playload.key] = playload.val
    },
    change_groups_detail: (state, playload) => {
        state.groups_detail[playload.puid] = playload.val
    },
    change_group_puid: (state, val) => {
        state.group_puid = val
    },
    change_group_trans: (state, val) => {
        state.groups_detail[state.group_puid]['is_trans'] = val
    },
    change_group_target: (state, val) => {
        state.groups_detail[state.group_puid]['target_group'] = val
    },
    change_group_white: (state, val) => {
        state.groups_detail[state.group_puid]['white'] = val
    },
    change_rule: (state, val) => {
        if (val.length > 0) {
            for (let each of val) {
                each.edit = false
                each.group = state.groups_detail[state.group_puid].group_name
            }
        }
        state.groups_detail[state.group_puid]['rule_list'] = val
    },
    change_robot_info: (state, val) => {
        state.info = val
    },
    change_time: (state, val) => {
        state.info.time = val
    }
}

const actions = {
    get_group_list: ({ state, commit }, force) => {
        if (state.login.status === 2) {
            let now = new Date().getTime()
            if (force || now - state.update_time.group_list > 30000) {
                axios.get(`${state.host}/api/groups/`)
                    .then(msg => {
                        commit('change_group_list', msg.data)
                    })
                commit('change_update_time', { key: 'group_list', val: now })
            }
        }
    },
    get_login_status: ({ state, commit }) => {
        axios.get(`${state.host}/api/login/status/`)
            .then(msg => {
                commit('change_login', msg.data)
                if (msg.data.status !== 2) {
                    router.push('/')
                }
            })
    },
    get_robot_info: ({ state, commit }) => {
        if (state.login.status === 2) {
            axios.get(`${state.host}/api/info/`)
                .then(msg => {
                    let data = msg.data
                    let info = {}
                    info.name = data.name
                    info.pic_src = data.pic_path
                    info.delay = data.delay
                    info.groups_num = data.group_num
                    info.trans_time = data.trans_count
                    info.trans_text = data.trans_text_count
                    info.trans_img = data.trans_pic_count
                    info.trans_groups = data.trans_group
                    info.reject_time = data.reject_count
                    commit('change_robot_info', info)
                    commit('change_trans_status', data.trans_swith)
                    commit('change_time', data.time)
                })
        }
    },
    get_group: ({ state, commit }, playload) => {
        let puid = playload.puid
        let force = playload.force
        let now = new Date().getTime()
        if (force || !state.update_time[puid] || now - state.update_time[puid] > 60000) {
            commit('change_loading', 1)
            axios.post(
                    `${state.host}/api/group/`,
                    qs.stringify({ puid: puid })
                )
                .then(msg => {
                    let data = msg.data
                    if (data.res) {
                        let group_detail = {}
                        group_detail.group_member_list = data.member
                        group_detail.pic_src = data.avatar
                        group_detail.group_name = data.name
                        group_detail.people_num = data.people_num
                        group_detail.is_owner = data.is_owner
                        group_detail.is_trans = data.is_trans
                        commit('change_groups_detail', { puid: puid, val: group_detail })
                        commit('change_group_puid', puid)
                        commit('change_rule', data.rule)
                        commit('change_group_target', data.target_group)
                        commit('change_loading', 0)
                        commit('change_group_white', data.white)
                    } else {
                        commit('change_loading', 2)
                    }
                })
            commit('change_update_time', { key: puid, val: now })
        } else {
            commit('change_group_puid', puid)
        }
    },
    switch_group_trans: ({ state, commit }, val) => {
        if (state.group_puid) {
            axios.post(`${state.host}/api/group/trans/`, qs.stringify({ puid: state.group_puid, val: val }))
                .then(msg => {
                    if (msg.data.res) {
                        commit('change_group_trans', val)
                    }
                })
        }
    },
    set_target_group: ({ state, commit, dispatch }, target) => {
        target = JSON.stringify(target)
        commit('change_loading', 1)
        axios.post(`${state.host}/api/group/target/`, qs.stringify({ puid: state.group_puid, target: target }))
            .then(msg => {
                setTimeout(() => {
                    dispatch('get_group', { puid: state.group_puid, force: true })
                }, 100)
            })
    },
    set_white: ({ state, commit, dispatch }, white) => {
        white = JSON.stringify(white)
        commit('change_loading', 1)
        axios.post(`${state.host}/api/group/white/`, qs.stringify({ puid: state.group_puid, white: white }))
            .then(msg => {
                setTimeout(() => {
                    dispatch('get_group', { puid: state.group_puid, force: true })
                }, 100)
            })
    },
    set_rule: ({ state, commit, dispatch }, rules) => {
        rules = JSON.stringify(rules)
        commit('change_loading', 1)
        axios.post(`${state.host}/api/group/rule/`, qs.stringify({ puid: state.group_puid, rules: rules }))
            .then(msg => {
                setTimeout(() => {
                    dispatch('get_group', { puid: state.group_puid, force: true })
                }, 100)
            })
    },
    del_member: ({ state, commit, dispatch }, members) => {
        members = JSON.stringify(members)
        commit('change_loading', 1)
        axios.post(`${state.host}/api/group/remove/`, qs.stringify({ puid: state.group_puid, members: members }))
            .then(msg => {
                setTimeout(() => {
                    dispatch('get_group', { puid: state.group_puid, force: true })
                }, 100)
            })
    }
}

export default {
    state,
    mutations,
    actions
}