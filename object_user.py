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

class ObjectUser(JSONEncoder):
    
    def __init__(self, i, x, y, m=0, r=0):
        self.Id = i
        self.PosX = x
        self.PosY = y
        self.Map = m
        self.RollDice = r
        self.Objects = {}
        
    def set_position(self, x, y):
        self.PosX = x
        self.PosY = y
        
    def add_key(self, idx):
        self.Objects.append(idx)
        
    def remove_key(self, idx):
        self.Objects.remove(idx)