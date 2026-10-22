import time
from http.server import BaseHTTPRequestHandler, HTTPServer

class PauseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Проверяем, что путь начинается с /pause
        if self.path.startswith('/pause'):
            parts = self.path.split('&')
            
            if len(parts) == 2:
                try:
                    # Извлекаем секунды и конвертируем в число
                    seconds = float(parts[1])
                    
                    # Ждем указанное количество секунд
                    time.sleep(seconds)
                    
                    # Формируем и отправляем успешный ответ 200
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(f"Paused for {seconds}s\n".encode('utf-8'))
                    return
                    
                except (ValueError, TypeError):
                    # Если не удалось конвертировать в число, возвращаем 500
                    self.send_response(500)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b"Server Error: Delay must be a number\n")
                    return
        
        # Если путь не /pause или нет символа &, тоже возвращаем 500
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Server Error: Invalid request format. Use /pause&<seconds>\n")

def run_server():
    port = 3355
    server_address = ('', port)
    httpd = HTTPServer(server_address, PauseHandler)
    print(f"Starting server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
