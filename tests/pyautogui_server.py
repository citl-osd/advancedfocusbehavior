##############
# DEPRECATED #
##############

import pyautogui
import pygetwindow

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib


class PyAutoGuiHandler(BaseHTTPRequestHandler):
    """"""
    def do_GET(self):
        path, querystr = self.path.split('?', 1)
        query_params = {}
        for param in querystr.split('&'):
            k, v = param.split('=', 1)
            query_params[k] = v

        code, msg = (200, 'OK')

        try:
            #pygetwindow.getWindowsWithTitle(target)[0].focus()
            if path == '/type':
                pyautogui.typewrite(query_params['keys'])

            elif path == '/press':
                pyautogui.press(query_params['key'])

            elif path == '/hotkey':
                pyautogui.hotkey(*json.loads(query_params['keys']))

            else:
                raise KeyError('Invalid route')

        except Exception as e:
            code, msg = (500, str(e))

        finally:
            self.send_response(code, message=msg)
            self.end_headers()


if __name__ == '__main__':
    HTTPServer(('localhost', 8090), PyAutoGuiHandler).serve_forever()
