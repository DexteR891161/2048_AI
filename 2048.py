import pygame
import random
import numpy as np
import time

pygame.init()
win = pygame.display.set_mode((400,400))
pygame.display.set_caption("2048")
font=pygame.font.SysFont('clearsans',20,1)
font_=pygame.font.SysFont('clearsans',50,1)

def get_empty_tiles(board):
    #board=np.transpose(board)
    return np.argwhere(board==0)
def evaluate(board):
    '''weight_matrix1=np.array([[4**6,4**5,4**4,4**3],
                            [4**5,4**4,4**3,4**2],
                            [4**4,4**3,4**2,4**1],
                            [4**3,4**2,4**1,4**0]])
    weight_matrix2=np.array([[7,6,5,4],
                            [6,5,4,3],
                            [5,4,3,2],
                            [4,3,2,1]])
    weight_matrix3=np.array([[4**15,4**14,4**13,4**12],
                            [4**8,4**9,4**10,4**11],
                            [4**7,4**6,4**5,4**4],
                            [4**0,4**1,4**2,4**3]])'''
    weight_matrix4=np.array([[2**15,2**14,2**13,2**12],
                            [2**8,2**9,2**10,2**11],
                            [2**7,2**6,2**5,2**4],
                            [2**0,2**1,2**2,2**3]])
    eval=np.sum(weight_matrix4*np.transpose(board))
    #if check_game_over(board):
    #return -eval
    return eval
def get2_4():
    num=random.randrange(0,10,1)
    if num>8:
        return 4
    return 2
def add_tile(grid_):
    option=[]
    for i in range(4):
        for j in range(4):
            if grid_[i][j]==0:
                option.append((i,j))
    if len(option)>0:
        choice=random.choice(option)
        grid_[choice[0]][choice[1]]=get2_4()
    return grid_
def slide_left(grid_):
    for i,line in enumerate(grid_):
        count=0
        for j in range(4):
            if line[j]!=0:
                grid_[i][count]=line[j]
                count+=1
        while(count<4):
            grid_[i][count]=0
            count+=1
    return grid_
def slide_right(grid_):
    for i,line in enumerate(grid_):
        count=3
        j=3
        while(j>=0):
            if line[j]!=0:
                grid_[i][count]=line[j]
                count-=1
            j-=1
        while(count>=0):
            grid_[i][count]=0
            count-=1
    return grid_
def combine_right(grid_):
    for i,line in enumerate(grid_):
        j=3
        flag=False
        while(j>0):
            if line[j]==line[j-1]:
                grid_[i][j]=2*line[j]
                grid_[i][j-1]=0
                grid_=slide_right(grid_)
                flag=True
            j-=1
    return flag,grid_
def combine_left(grid_):
    flag=False
    for i,line in enumerate(grid_):
        for j in range(3):
            if line[j]==line[j+1]:
                grid_[i][j]=2*line[j]
                grid_[i][j+1]=0
                grid_=slide_left(grid_)
                flag=True
    return flag,grid_
def check_game_over(array):
    if 0 not in array:
        flag1=False
        flag2=False
        for line in array:
            for i in range(3):
                if line[i]==line[i+1]:
                    flag1=True
        array=array.transpose()
        for line in array:
            for i in range(3):
                if line[i]==line[i+1]:
                    flag2=True

        if flag1 or flag2:
            return False
        else:
            return True
    else:
        return False
def choose_color(num):
    if num==2:
        return 238,228,218
    elif num==4:
        return 237,224,200
    elif num==8:
        return 242,177,121
    elif num==16:
        return 245,149,99
    elif num==32:
        return 246,124,95
    elif num==64:
        return 246,94,59
    elif num==128:
        return 237,207,114
    elif num==256:
        return 237,204,97
    elif num==512:
        return 237,200,80
    elif num==1024:
        return 237,197,63
    elif num==2048:
        return 237,194,46
    else:
        return 10,10,10
def take_action(key_pressed,grid_):
    if key_pressed==1:
        grid_=grid_.transpose()
        grid_=slide_left(grid_)
        com,grid_=combine_left(grid_)
        grid_=grid_.transpose()

    elif key_pressed==2:
        grid_=grid_.transpose()
        grid_=slide_right(grid_)
        com,grid_=combine_right(grid_)
        grid_=grid_.transpose()

    elif key_pressed==3:
        grid_=slide_left(grid_)
        com,grid_=combine_left(grid_)

    elif key_pressed==4:
        grid_=slide_right(grid_)
        com,grid_=combine_right(grid_)
    return grid_
#BOARD=+1
#AI=-1
def smart(state,depth,agent):
    if depth==0 or check_game_over(state):
        return [0,evaluate(state)]
    if agent==1:
        score=[0,0]
        sum=0
        empty_tiles=get_empty_tiles(state)
        for tile in empty_tiles:
            state[tile[0]][tile[1]]=2
            score=smart(state.copy(),depth-1,-1)
            sum+=0.9*score[1]
            state[tile[0]][tile[1]]=4
            score=smart(state.copy(),depth-1,-1)
            sum+=0.1*score[1]
            state[tile[0]][tile[1]]=0
        return [0,sum/len(empty_tiles)]
    elif agent==-1:
        best=[0,0]
        score=[0,0]
        newState=state.copy()
        for i in range(1,5):
            state=take_action(i,newState.copy())
            if not np.array_equal(state,newState):
                score=smart(state.copy(),depth-1,1)
                score[0]=i
                if score[1]>best[1]:
                    best=score
        return best

def main():
    x_offset=100
    y_offset=100
    grid=np.zeros((4,4))
    last_grid=np.zeros((4,4))
    run=True
    over=False
    play=False
    runAi=False

    grid=add_tile(grid)
    while run:
        key_pressed=0
        mouse_key=pygame.mouse.get_pressed()
        x,y=pygame.mouse.get_pos()
        if mouse_key[0]:
            if (x>100 and x<170) and (y>70 and y<90):
                play=True
                runAi=False
            if (x>230 and x<300) and (y>70 and y<90):
                runAi=True
                play=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if play:
            pygame.time.delay(150)
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                key_pressed=1

            if key[pygame.K_RIGHT]:
                key_pressed=2

            if key[pygame.K_UP]:
                key_pressed=3

            if key[pygame.K_DOWN]:
                key_pressed=4
        if runAi:
            if len(get_empty_tiles(grid))<4:
                depth=5
            else:
                depth=4
            key_pressed=smart(grid.copy(),depth,-1)[0]

        grid=take_action(key_pressed,grid)

        if not np.array_equal(last_grid,grid):
            grid=add_tile(grid)

        win.fill((255,255,255))
        win.blit(font_.render("2048",2,(200,0,0)),(150,20))
        pygame.draw.rect(win,(0,0,0),(100,70,70,20),1)
        pygame.draw.rect(win,(0,0,0),(230,70,70,20),1)
        win.blit(font.render("PLAY",2,(0,0,0)),(115,73))
        win.blit(font.render("RUN AI",2,(0,0,0)),(240,73))
        pygame.draw.rect(win,(0,0,0),(x_offset-1,y_offset-1,202,202),1)

        for i in range(4):
            for j in range(4):
                if grid[i][j]!=0:
                    r,g,b=choose_color(grid[i][j])
                    pygame.draw.rect(win,(r,g,b),((i*50)+x_offset,(j*50)+y_offset,50,50))
                    if grid[i][j]<5:
                        t_r,t_g,t_b=(0,0,0)
                    else:
                        t_r,t_g,t_b=(255,255,255)
                    text_score=font.render(str(int(grid[i][j])),1,(t_r,t_g,t_b))
                    if grid[i][j]==512:
                        offset=15
                    elif grid[i][j]>=1024:
                        offset=10
                    else:
                        offset=20
                    win.blit(text_score,(x_offset+(i*50)+offset,y_offset+(j*50)+20))
        pygame.display.update()
        over=check_game_over(grid)
        if over:
            print("Game Over")
            run=False
        last_grid=grid.copy()

    time.sleep(2)
    print(grid.transpose())
    pygame.quit()

main()
