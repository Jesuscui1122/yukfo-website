# -*- coding: utf-8 -*-
"""静态服务器：无扩展名路径回退到 .html（模拟 Cloudflare 行为）"""
import http.server, socketserver, os, sys

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory='.', **kw)
    def do_GET(self):
        p = self.path.split('?')[0]
        if p == '/' or (not os.path.splitext(p)[1] and not p.endswith('/')):
            cand = p.lstrip('/') + '.html'
            if os.path.exists(cand):
                self.path = '/' + cand
        return super().do_GET()
    def log_message(self, *a): pass

os.chdir(sys.argv[1] if len(sys.argv) > 1 else '.')
# ThreadingTCPServer: 浏览器会并行开连接（预连接不发请求也会占住 handler），
# 单线程版会被一个挂起连接卡死全部请求
socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("127.0.0.1", 8897), H) as httpd:
    httpd.daemon_threads = True
    httpd.serve_forever()
