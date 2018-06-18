import random
from tkinter import *

#Глобальные переменные
WIDTH = 960
HEIGHT = 600
SEGMENT_SIZE = 20
BALL_RADIUS = 30
IN_GAME = True #Переменная, отвечающая за состояние игры
counter = 3
dictionary = {0: "red", 1: "orange", 2: "yellow", 3: "green", 4: "aqua", 5: "blue", 6: "purple"}
#Класс сегмента змейки (возможно вынести в отдельный файл)

class Segment(object):
    def __init__(self, x, y, color):
        self.instance = c.create_rectangle(x, y, x+SEGMENT_SIZE, y+SEGMENT_SIZE, fill=color)
#Класс змейки 
class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        #список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1),
                        "Up": (0, -1),
                        "Left": (-1, 0),
                        "Right": (1, 0)}
        self.mappingUP = {"Up": (0, -1),
                          "Left": (-1, 0),
                          "Right": (1, 0)}
        self.mappingDOWN = {"Down": (0, 1),
                          "Left": (-1, 0),
                          "Right": (1, 0)}
        self.mappingRIGHT = {"Up": (0, -1),
                          "Left": (-1, 0),
                          "Down": (0, 1)}
        self.mappingLEFT = {"Up": (0, -1),
                          "Down": (0, 1),
                          "Right": (1, 0)}
        #изначально змейка двигается вправо
        self.vector = self.mapping["Down"]

    def move(self):
        """Двигает змейку в заданном направлении"""
        #перебираем все сегменты кроме первого
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            #задаем каждому сегменту позицию сегмента стоящего после него
            c.coords(segment, x1, y1, x2, y2)
            #получаем координаты сегмента перед "головой"
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
            #помещаем голову в направлении указанном в векторе движения
        c.coords(self.segments[-1].instance,
                         x1 + self.vector[0]*SEGMENT_SIZE,
                         y1 + self.vector[1]*SEGMENT_SIZE,
                         x2 + self.vector[0]*SEGMENT_SIZE,
                         y2 + self.vector[1]*SEGMENT_SIZE)

    def change_direction(self, event):
        """Изменяет направление движения змейки"""
        #event передаст символ нажатой клавиши
        #и если эта клавиша в доступных направлениях
        #изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self, color):
        """Добавляет сегмент змейке"""
        #определяем последний сегмент
        global counter
        last_seg = c.coords(self.segments[0].instance)

        #определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - SEGMENT_SIZE
        y = last_seg[3] - SEGMENT_SIZE
        #добавляем змейке еще один сегмент в заданных координатах

        self.segments.insert(0, Segment(x, y, color))
        counter += 1

root = Tk()
root.title("Начало игры")
play = PhotoImage(file = 'field.gif')
l = Label(root, image = play)
l.pack()
def but_onoff(event, button):
    if button == "Справка":
        but["text"] = "Цель игры - перемещаться по полю, съедая красные кружки.\n" \
                      "Для перемещения по полю используются клавиши со стрелками.\n" \
                      "Игра закончится в 3 случаях:\n" \
                      "1) Змейка врежется в стенку;\n" \
                      "2) Змейка съест свой хвост;\n" \
                      "3) Змейка врежется в саму себя;\n" \
                      "4) Змейка заполнит собой всё поле.(Этого еще никто не видел!)\n" \
                      "Чтобы приступить к игре, закройте это окно, \n" \
                      "затем закройте окно с полем" \
                      " и нажмите левой клавишей мыши на окно со змейкой.\n" \
                      "Желаем удачи и приятной игры!"



import tkinter
root = tkinter.Tk()
but = tkinter.Button(root, text="Справка", width=70, height=15, bg="green", fg="white")
but.pack(side=tkinter.RIGHT)
but.bind("<Button-1>", lambda event: but_onoff(event, but["text"]))
root.mainloop()

root.mainloop()

#Создаем окно
root = Tk()
#Устанавливаем название окна
root.title("Python Snake")

#Создаем экземпляр класса Canvas и заливаем все зеленым
c = Canvas(root, width=WIDTH, height=HEIGHT)

#Создаем фон поля
img = PhotoImage(file="pole.gif")

c.create_image(0, 0, anchor=NW, image=img)
c.grid()
#Наводим фокус на Canvas, чтобы ловить нажатия клавиш
c.focus_set()


#создаем набор сегментов
segments = [Segment(SEGMENT_SIZE, SEGMENT_SIZE, dictionary.get(2)),
            Segment(SEGMENT_SIZE*2, SEGMENT_SIZE, dictionary.get(1)),
            Segment(SEGMENT_SIZE*3, SEGMENT_SIZE, dictionary.get(0))]
#сама змейка
s = Snake(segments)
#привяжем метод класса Snake change_direction() к Canvas
c.bind("<KeyPress>", s.change_direction)

def create_block():
    """создает блок в случайной позиции на карте"""
    global BLOCK
    posx = SEGMENT_SIZE * random.randint(1, (WIDTH-SEGMENT_SIZE) / SEGMENT_SIZE)
    posy = SEGMENT_SIZE * random.randint(1, (HEIGHT-SEGMENT_SIZE) / SEGMENT_SIZE)

    BLOCK = c.create_oval(posx, posy,
                          posx + SEGMENT_SIZE,
                          posy + SEGMENT_SIZE,
                          fill="red")

def main():
    global IN_GAME
    global counter
    if IN_GAME:
        #двигаем змейку
        s.move()
        #определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        #столкновение с границами экрана
        if x1 < 0 or x2 > WIDTH or y1 <0 or y2 > HEIGHT:
            IN_GAME = False
        #поедание яблок
        elif head_coords == c.coords(BLOCK):



            while counter < 8:
                if counter == 7:
                    counter = 0
                s.add_segment(dictionary.get(counter))
                break

            c.delete(BLOCK)
            create_block()

        #самоедство
        else:
            #Проходим по всем сегментам змеи
            for index in range(len(s.segments)-1):
                if c.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False
        root.after(100, main)
    #если не в игре выводим сообщение о проигрыше
    else:
        c.create_text(WIDTH/2, HEIGHT/2,
                      text = "ИГРА ОКОНЧЕНА!",
                      font = "Arial 20",
                      fill = "red")

create_block()
main()

#Запускаем окно
root.mainloop()
