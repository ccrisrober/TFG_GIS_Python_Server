'''
Copyright (c) 2015, maldicion069 (Cristian Rodríguez) <ccrisrober@gmail.con>
//
Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
//
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''
import SocketServer
import threading

import key_object
import object_user
import map
import json

def jdefault(o):
    return o.__dict__

# Preguntamos si es juego o test
mode = raw_input('[S/s] Server Mode / [] Test Mode:')
is_game = False
if mode == "s" or mode == "S":
    is_game = True

print(is_game)

lock_positions = threading.Lock()
lock_sockets = threading.Lock()

positions = {}
sockets = {}

maps = []

keys = {
   "Red": key_object.KeyObject(1, 5*64, 5*64, "Red"),
   "Blue": key_object.KeyObject(2, 6*64, 5*64, "Blue"),
   "Yellow": key_object.KeyObject(3, 7*64, 5*64, "Yellow"),
   "Green": key_object.KeyObject(4, 8*64, 5*64, "Green")
}

config = json.loads(open('data.json').read())

map_0 = ""
keys_0 = []

for line in config["map"]:
    map_0 += line
for key in config["keys"]:
    keys_0.append(keys[key])

maps.append(map.Map(config["id"],
            map_0,
            config["width"],
            config["height"],
            keys_0))

print (json.dumps(maps[0], default=jdefault))

class TCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        msg = ""
        print (len(sockets))

        exit = False

        while(1):
            msg = self.request.recv(1024).decode('UTF-8')
            print (msg[0:-1])
            msg_ = None
            try:
                msg_ = json.loads(msg)
            except Exception as e:
                print ("Error({0}): {1}".format(e.errno, e.strerror))
                continue

            action = msg_["Action"]

            print (action)

            if action == "initWName":
                obj_user = object_user.ObjectUser(self.client_address[1], 5*64, 5*64)

                info = json.dumps({"Action": "sendMap", "Map": maps[0],
                            "X": obj_user.PosX, "Y": obj_user.PosY, "Id": obj_user.Id,
                            "Users": positions}, default=jdefault) + "\n"

                print(info)

                lock_positions.acquire()
                positions[self.client_address[1]] = obj_user
                lock_positions.release()

                self.request.send(info.encode("utf-8"))


                if is_game:
                    msg = json.dumps({
                        "Action": "new", "Id": obj_user.Id, "PosX": obj_user.PosX, "PosY": obj_user.PosY
                    }, default=jdefault).encode("utf-8")

                lock_sockets.acquire()
                sockets[self.client_address[1]] = (self.request)
                lock_sockets.release()

            elif action == "move":
                lock_positions.acquire()
                positions[self.client_address[1]].set_position(msg_["Pos"]["X"], msg_["Pos"]["Y"])
                lock_positions.release()
                if not is_game:
                    self.request.send(msg.encode("utf-8"))
            elif action == "position":
                pos = json.dumps(positions[self.client_address[1]])
                self.request.send(pos.encode("utf-8"))
                continue
            elif action == "exit":
                # Erase socket from positions!!
                lock_positions.acquire()
                if self.client_address[1] in positions: del positions[self.client_address[1]]
                lock_positions.release()
                # Erase socket!!
                lock_sockets.acquire()
                del sockets[self.client_address[1]]
                if not is_game:
                    self.request.send(json.dumps({"Action": "exit", "Id": "Me"}).encode("utf-8"))
                exit = True
                lock_sockets.release()
                if not is_game:
                    break
                if is_game:
                    msg = json.dumps({"Action": "exit", "Id": self.client_address[1]})
            if is_game:
                msg = msg.encode("utf-8")

                for _, sock in sockets.iteritems():
                    if sock != self.request:
                        sock.send(msg)
                # self.request.send(msg)
            if exit:
                break

class ThreadServer(SocketServer.ThreadingMixIn, SocketServer.ForkingTCPServer):
    pass

if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8091
    server = ThreadServer((host, port), TCPServerHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print ("Server start")
