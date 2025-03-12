// TODO: 时间格式修改为月日时分
export function formulate_time(time) {
    var date = new Date(time)
    return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate()
}

export function formulate_time_MDHM(time) {
    var date = new Date(time)
    return (date.getMonth() + 1) + "月" + date.getDate() + "日" + date.getHours() + "时" + date.getMinutes() + "分"
}