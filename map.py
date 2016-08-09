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

from json import JSONEncoder

real_objects = {}

class Map(JSONEncoder):

    def __init__(self, i, mf, w, h, ko):
        self.Id = i
        self.MapFields = mf
        self.Width = w
        self.Height = h
        self.KeyObjects = {}
        for k in ko:
            self.KeyObjects[k.Id] = k
            real_objects[k.Id] = k

    def add_key(self, idx, px, py):
        real_objects[idx].set_position(px, py)
        ko = real_objects[idx]
        self.KeyObjects[idx] = ko
        return ko
    
    def remove_key(self, idx):
        del self.KeyObjects[idx]
        return real_objects[idx]