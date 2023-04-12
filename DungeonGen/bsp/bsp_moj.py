# -*- coding: UTF-8 -*-

import random
import time
from datetime import datetime
from utilitaires import generate_random_string


# from itertools import chain

# import sys
from classes.Room import room


class leaf():

    MIN_LEAF_SIZE = 80
    MAX_DEPTH = 5

    def __init__(self, origin, width, height, depth=1):
        self.x, self.y = origin
        self.height = height
        self.width = width
        self.leftBIS = None
        self.r = None
        self.depth = depth
        self.room = room((self.x, self.y), self.width, self.height, "room")
        # 0 for vertical, 1 for horizontal split, None for not split
        self.split_orientation = None

    def __iter__(self):
        if self.leftBIS:
            yield from self.leftBIS
        yield self
        if self.r:
            yield from self.r
        # yield from self.leaves()

    def split(self):
        # split the leaf in two, unless the size of the leaf is too small
        h_less = self.height <= self.MIN_LEAF_SIZE
        w_less = self.width <= self.MIN_LEAF_SIZE
        self.room = room((self.x, self.y), self.width, self.height, "Room " +
                         str(random.randint(0, 100)))

        if h_less and w_less:
            return
        elif w_less:
            self.split_h()
        elif h_less:
            self.split_v()
        elif random.choice((0, 1)) == 0:
            self.split_v()
        else:
            self.split_h()
        return

    def split_v(self):
        # spliting vertically, on x-axis
        if self.depth > self.MAX_DEPTH:
            return

        movx = int(random.uniform(0.45*self.width, 0.55*self.width))
        if self.width-movx < self.MIN_LEAF_SIZE:
            return

        self.split_orientation = 0

        self.leftBIS = leaf((self.x,
                             self.y),
                            movx,
                            self.height,
                            self.depth + 1)

        self.r = leaf((self.x + movx,
                       self.y),
                      self.width - movx,
                      self.height,
                      self.depth + 1)

        self.leftBIS.split()
        self.r.split()
        # print("successful vertical division")

    def split_h(self):
        # splitting horizontally, on y-axis. L is above, R is below.
        if self.depth > self.MAX_DEPTH:
            return

        movy = int(random.uniform(0.45*self.height, 0.55*self.height))
        if self.height-movy < self.MIN_LEAF_SIZE:
            return

        self.split_orientation = 1

        self.leftBIS = leaf((self.x,
                             self.y),
                            self.width,
                            movy,
                            self.depth + 1)

        self.r = leaf((self.x, self.y+movy),
                      self.width,
                      self.height - movy,
                      self.depth + 1)

        self.leftBIS.split()
        self.r.split()
        # print("successful horizontal division")

    def packit(self):
        # packs the leaf data
        return (self.x, self.y, self.width, self.height)

    def leaves(self):
        # returns the leaf rooms in order
        if self.leftBIS is None and self.r is None:
            # return [self.packit()]
            return [self.room]
        elif self.leftBIS is None:
            return self.r.leaves()
        elif self.r is None:
            return self.leftBIS.leaves()
        else:
            return self.leftBIS.leaves() + self.r.leaves()


class dungeon:

    # variable statique
    level_dungeon = 0

    def __init__(self,
                 width,
                 height,
                 seed=None):
        if seed is None:
            self.seed = random.randint(5, int(round(time.time())))
        else:
            self.seed = None

        random.seed(self.seed)
        self.tree = leaf((0, 0), width, height)
        self.tree.split()

    def __iter__(self):
        i = self.tree.__iter__()
        return i
