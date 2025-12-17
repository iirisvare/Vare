import pygame 
import sys 

# initializing the constructor 
pygame.init() 

#üldsätted
res = (1080,720) 
screen = pygame.display.set_mode(res) 
pygame.display.set_caption('VARE katse')
fps = 60
fpsClock = pygame.time.Clock()

#ekraani omaduste salvestamine
width = screen.get_width() 
height = screen.get_height() 

# menüü üldsätted 
menu = True
# nupu sätted
nupu_fondi_varv = (255,255,255) 
nupu_font = pygame.font.SysFont('Corbel',35) 
nupp_varv = (100,100,100) 
nupp_selected_varv = (170,170,170) 
nupu_tekst = nupu_font.render('Exit' , True , nupu_fondi_varv) 


objects = []


class Button():
    def __init__(self, x, y, width, height, buttontext, onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.buttontext = buttontext
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.fillColors = {
            'normal': "#4c3dcd",
            'hover': "#8E8CFF",
            'pressed': "#CECDFF",
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)



class Exit(Button):

while True :
    while menu == True :
        screen.fill((0, 0, 88))
        for ev in pygame.event.get(): 
            
            if ev.type == pygame.QUIT: 
                pygame.quit() 
                
            #checks if a mouse is clicked 
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                
                #if the mouse is clicked on the 
                # button the game is terminated 
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                    pygame.quit() 
        mouse = pygame.mouse.get_pos()
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
            pygame.draw.rect(screen,nupp_selected_varv,[width/2,height/2,140,40]) 
            
        else: 
            pygame.draw.rect(screen,nupp_varv,[width/2,height/2,140,40]) 
        
        # superimposing the text onto our button 
        screen.blit(nupu_tekst , (width/2+50,height/2)) 
        
        # updates the frames of the game 
        pygame.display.update() 

def joonista_tekst(tekst, font, värv, y):
    pilt = font.render(tekst, True, värv)
    rect = pilt.get_rect(center=(laius // 2, y))
    aken.blit(pilt, rect)

# menüü sätted
class Nupp():
    def __init__(self, x, y, tekst) :
        self.laius = 90
        self.kõrgus = 40
        self.pind = pygame.Surface((self.laius, self.kõrgus))
        self.rect = pygame.Rect(x, y, self.laius, self.kõrgus)
        self.värvid = {'normal': "#4c3dcd", 'hover': "#8E8CFF", 'pressed': "#CECDFF",}
        self.tekst = font.render(tekst, )

    else:
        # menüü
        kell.tick(fps)
        aken.fill(tumesinine)


        # pealkiri
        joonista_tekst("The Catfather", suur_font, kollane, 150)

        if mäng_lõppes_sõnum:
            joonista_tekst(mäng_lõppes_sõnum, väike_font, valge, 230)
            joonista_tekst("Vajuta ükskõik millist klahvi, et uuesti proovida.", väike_font, punane, 280)
        else:
            # alguse juhised
            joonista_tekst("Kogu kalu enne kui aeg otsa saab.", väike_font, valge, 230)
            joonista_tekst("Vajuta ükskõik millist klahvi, et alustada.", väike_font, punane, 280)

    pygame.display.flip()  


def alusta_mäng() :
    # algväärtustamine uue mängu jaoks
    global mäng_aktiivne, mäng_lõppes_sõnum, praegune_tase, kalu_kogutud, taseme_algus_aeg, platvormid, kalad, mängija_grupp, kõrgus
    mäng_aktiivne = True
    mäng_lõppes_sõnum = ""
    praegune_tase = 1
    kalu_kogutud = 0

    info = taseme_info(praegune_tase - 1)
    taseme_aeg = info["aeg"]
    kalu_vaja = info["eesmärk"]
    taseme_algus_aeg = pygame.time.get_ticks()

    platvormid = loo_platvormid()
    kalad = genereeri_kalad(kalu_vaja + 5, platvormid)

    mängija_grupp.empty()
    mängija_grupp.add(Mängija(100, kõrgus - 200))