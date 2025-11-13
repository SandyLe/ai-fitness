from flask import Flask, redirect, url_for, session, render_template, request, g
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # 假设 'user' 存储在 session 中表示登录状态
            return redirect(url_for('auth.login', next=request.url))  # 重定向到登录页面，并传递当前请求的 URL 作为 next 参数以便登录后重定向回原页面
        return f(*args, **kwargs)
    return decorated_function