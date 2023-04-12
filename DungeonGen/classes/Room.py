import random


class room:
    # generates a room inside a leaf
    MIN_ROOM_SIZE = 40

    def __init__(self,
                 origin,
                 width,
                 height,
                 name=None):
        self.x, self.y = origin
        self.width = width
        self.height = height
        self.name = "room"
        # calcule le centre de la room
        self.center = (self.x + self.width // 2, self.y + self.height // 2)

        # move the origin
        movx = int(random.triangular(1, 0.4*self.width, 0.05*self.width))
        movy = int(random.triangular(1, 0.4*self.height, 0.05*self.height))
        self.x += movx
        self.y += movy

        # reduce size
        # movwidth = int(random.uniform(movx, self.width-movx))
        # movheight = int(random.uniform(movy, self.height-movy))
        movwidth = int(random.triangular(movx, self.width-movx,
                                         movx+0.05*(self.width-movx)))
        movheight = int(random.triangular(movy, self.height-movy,
                                          movy+0.05*(self.height-movy)))
        self.width -= movwidth
        self.height -= movheight

        if self.width < self.MIN_ROOM_SIZE:
            self.width = self.MIN_ROOM_SIZE
        if self.height < self.MIN_ROOM_SIZE:
            self.height = self.MIN_ROOM_SIZE

    def __str__(self):
        return f"Room(name={self.name}\n,\
                        x={self.x}\n,\
                        y={self.y}\n,\
                        width={self.width}\n,\
                        height={self.height}\n)"

    def packit(self):
        # packs the room data
        """
        print(" ")
        print("valeur de self.x depuis def packit: " + str(self.x))
        print("valeur de self.y depuis def packit: " + str(self.y))
        print("valeur de self.width depuis def packit: " + str(self.width))
        print("valeur de self.height depuis def packit:" + str(self.height))
        print("valeur de self.center depuis def packit:" + str(self.center))
        """

        return (self.x,
                self.y,
                self.width,
                self.height)
