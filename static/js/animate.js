// 获取元素计算后的属性
function getStyle(element, attr) {
    return window.getComputedStyle ? window.getComputedStyle(element, null)[attr] : element.currentStyle[attr];
}

// 封装建议缓动动画函数
function animate(element, obj, callback) {
    // 清除定时器
    clearInterval(element.timer);
    // 创建定时器
    element.timer = setInterval(function () {
        // 假设已经达到了目标值
        let flag = true;
        // 遍历对象
        for (let k in obj) {
            // 获取元素计算后的属性
            // 因为获取过来的属性带单位,我们需要将字符串转换为数字
            let current = parseInt(getStyle(element, k));
            // 获取目标值
            let target = obj[k];
            // 计算步进值
            let step = (target - current) / 10;
            // 对步进值进行取整
            step = step > 0 ? Math.ceil(step) : Math.floor(step);
            // 累加步进值
            current += step;
            // 将最终结果赋值给对应的属性
            element.style[k] = current + 'px';
            // 判断是否达到了目标值
            if (current !== target) {
                // 没有达到目标值,就让flag变为false
                flag = false;
            }
        }
        // 达到目标值,就清除定时器
        if (flag) {
            clearInterval(element.timer);
            callback() ? callback : null;
        }
    }, 20)
}