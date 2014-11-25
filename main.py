import sys, time, threading, curses, random

class Tui:
    def pos(self, x, y):
        sys.stdout.write("\033[%d;%dH" % (y, x))
        sys.stdout.flush()
    def clear(self):
        print("\033[2J")

class Snake:
    def __init__(self):
        self.reset()
        self.thread = threading.Thread(target = self.main)
        self.thread.start()

    def reset(self):
        self.width = 20
        self.height= 10
        self.sx = 10
        self.sy = 4
        self.tui = Tui()
        self.direction = 1        
        self.body = []
        self.loop = True
        self.setitem()

        for i in range(5):
            self.body.append((self.sx + 1, self.sy))
    
    def setitem(self):
        self.item = (random.randint(1, self.width), random.randint(1, self.height))

    def main(self):
        while self.loop:
            self.move()
            self.draw()
            time.sleep(0.2)

    def draw(self):
        self.tui.clear()
        self.tui.pos(0, self.height + 5)
        print(" q:quit")
        self.tui.pos(self.sx, self.sy)
        print("O")
        for (x, y) in self.body:   
            self.tui.pos(x, y)
            print("o")
        self.tui.pos(self.item[0], self.item[1])
        print("x")
        self.tui.pos(0, self.height+5)    

    def move(self):
        self.body.pop()
        self.body.insert(0, (self.sx, self.sy))     
        man = {
            1 : (lambda : (self.sx - 1, self.sy)),
            4 : (lambda : (self.sx + 1, self.sy)),
            2 : (lambda : (self.sx, self.sy - 1)),
            8 : (lambda : (self.sx, self.sy + 1))
        }
        (self.sx, self.sy) = man[self.direction]()
        if(self.sx < 1): self.sx = self.width
        if(self.sx > self.width): self.sx = 1
        if(self.sy < 1): self.sy = self.height
        if(self.sy > self.height): self.sy = 1
        if(self.sx == self.item[0] and self.sy == self.item[1]):
            self.setitem()
            self.body.append(self.body[-1])
        if (self.sx, self.sy) in self.body:
            self.reset()
        
    def stop(self):
        self.loop = False
        self.thread.join()

def curses_main(args):
    snake = Snake()
    curses.cbreak()
    curses.noecho()
    stdscr = curses.initscr()
    stdscr.keypad(True)
    while True:
        ky = stdscr.getch()
        if ky == curses.KEY_LEFT and snake.direction != 4 : snake.direction = 1
        elif ky == curses.KEY_DOWN and snake.direction != 2 : snake.direction = 8
        elif ky == curses.KEY_UP and snake.direction != 8 : snake.direction = 2
        elif ky == curses.KEY_RIGHT and snake.direction != 1 : snake.direction = 4
        elif ky == ord('q') : break
    snake.stop()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    curses.wrapper(curses_main)
