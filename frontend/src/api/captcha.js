import api from './index'

// 获取验证码
export function getCaptcha() {
    return api.get('/captcha/')
}