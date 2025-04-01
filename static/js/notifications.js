// WebSocket 连接
let notificationSocket = null;

// 获取CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 更新通知数量的函数
function updateNotificationCount() {
    const notificationCount = document.getElementById('notification-count');
    if (!notificationCount) {
        console.log('未找到通知计数元素');
        return;
    }

    console.log('开始获取通知数量...');
    fetch('/notifications/api/notifications/unread-count/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        console.log('收到响应:', response.status);
        if (!response.ok) {
            throw new Error('网络响应错误: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('收到数据:', data);
        if (data.count !== undefined) {
            updateNotificationBadge(data.count);
        } else {
            console.error('返回数据格式不正确:', data);
        }
    })
    .catch(error => {
        console.error('获取通知数量失败:', error);
    });
}

// 更新通知徽章
function updateNotificationBadge(count) {
    const notificationCount = document.getElementById('notification-count');
    if (!notificationCount) return;

    if (count > 0) {
        notificationCount.textContent = count;
        notificationCount.className = 'badge badge-danger';
    } else {
        notificationCount.textContent = '0';
        notificationCount.className = 'badge badge-light';
    }
}

// 初始化通知功能
function initNotifications() {
    console.log('初始化通知功能...');
    const notificationCount = document.getElementById('notification-count');
    if (!notificationCount) {
        console.log('未找到通知计数元素，可能未登录');
        return;
    }

    // 立即执行一次更新
    updateNotificationCount();

    // 设置定时器，每30秒更新一次
    const intervalId = setInterval(updateNotificationCount, 1000);
    console.log('已设置定时器，每1秒更新一次');

    // 页面关闭时清除定时器
    window.addEventListener('beforeunload', () => {
        clearInterval(intervalId);
        console.log('清除定时器');
    });
}

// 初始化 WebSocket 连接
function initWebSocket() {
    const notificationCount = document.getElementById('notification-count');
    if (!notificationCount) return;

    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const wsUrl = `${wsScheme}://${window.location.host}/ws/notifications/`;
    
    notificationSocket = new WebSocket(wsUrl);

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        updateNotificationBadge(data.count);
    };

    notificationSocket.onclose = function(e) {
        console.error('通知 WebSocket 连接已关闭');
        // 尝试重新连接
        setTimeout(initWebSocket, 5000);
    };

    // 连接成功后请求初始计数
    notificationSocket.onopen = function() {
        notificationSocket.send(JSON.stringify({
            'message': 'get_count'
        }));
    };
}

// 当文档加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM加载完成，开始初始化通知功能');
    initNotifications();
});

// 页面关闭时清理
window.addEventListener('beforeunload', function() {
    if (notificationSocket) {
        notificationSocket.close();
    }
}); 