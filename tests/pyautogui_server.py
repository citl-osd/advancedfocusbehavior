import pyautogui
import pygetwindow

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib


class PyAutoGuiHandler(BaseHTTPRequestHandler):
    """"""
    def do_GET(self):
        keys = urllib.parse.unquote(self.path[1:])

        code, msg = (200, 'OK')

        try:
            #pygetwindow.getWindowsWithTitle(target)[0].focus()
            pyautogui.typewrite(keys)

        except Exception as e:
            code, msg = (500, str(e))

        finally:
            self.send_response(code, message=msg)
            self.end_headers()


if __name__ == '__main__':
    HTTPServer(('localhost', 8090), PyAutoGuiHandler).serve_forever()
