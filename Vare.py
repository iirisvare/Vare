"""
Projekti teema:
Mäng, kus mängija peab piiratud aja jooksul koguma etteantud arvu kalu.
Kui ta saab vajalikud kalad kätte enne aja lõppu, liigub ta järgmisesse tasemesse,
kus nõuded muutuvad karmimaks – rohkem kalu ja vähem aega.
Aga kui ta ei jõua piisavalt kalu püüda, ilmub kass Moorits ja sööb ta ära.

Autorid:
   • Ellinor Usai
   • Iiris Vare

Eeskujuna kasutatud allikad:
   • Pygame'i dokumentatsioon
   • Geeks for Geeks
   • Kursuse materjalid
   
Muu oluline info:
Projekti idee tuli päriselus olemasolevast kassist Mooritsast, kes on tugevalt toidulembeline ja vallatu.
Mängu eesmärk on pakkuda meelelahutust, peletada igavust ning panna proovile mängija kannatlikkus kasside suhtes.
"""
import pygame
import sys
import random

pygame.init()

# mängu üldsätted
laius = 1020
kõrgus = 720
aken = pygame.display.set_mode((laius, kõrgus))  
pygame.display.set_caption("Projekt Vare")  
kell = pygame.time.Clock()  
fps = 60  

# värvid
valge = (255, 255, 255)
must = (0, 0, 0)
hall = (60, 60, 60)
lilla = (180, 80, 200)
kollane = (255, 220, 80)
punane = (230, 50, 70)
tumesinine = (10, 15, 40)

# fondid
suur_font = pygame.font.SysFont("bahnschrift", 52, True)  
väike_font = pygame.font.SysFont("bahnschrift", 24)  

# globaalsed muutujad
max_tasemeid = 5  
praegune_tase_number = 1
praegune_tase = None
tase_algus_aeg = 0
kalu_kogutud = 0
üleminek_millal = 0
mäng_aktiivne = False
mäng_lõppes_sõnum = ""
kas_vahekaart = False
tsükkel = True

# üldiselt kasutatud definitsioonid
def joonista_tekst(tekst, font, värv, y):
    pilt = font.render(tekst, True, värv)
    rect = pilt.get_rect(center=(laius // 2, y))
    aken.blit(pilt, rect)

def sulge_mäng():
    tsükkel = False
    pygame.quit()
    sys.exit()

def alusta_tase() :
    # paneme globaalsed muutujad nulli iga uue taseme alguses
    global mäng_aktiivne, kalu_kogutud, tase_algus_aeg, praegune_tase
    kalu_kogutud = 0
    tase_algus_aeg = pygame.time.get_ticks()
    praegune_tase = Tase(aken, praegune_tase_number)
    if mängija_grupp.sprite : # kontrollime, et ta on ikkagi olemas enne kui midagi teeme
        mängija_grupp.sprite.rect.topleft = (100, kõrgus - 200)
        Mängija.kiirus_x = 0
        Mängija.kiirus_y = 0
    mäng_aktiivne = True


def alusta_mäng() :
    # alustame mängu esimest korda
    global mäng_aktiivne, mäng_lõppes_sõnum, praegune_tase_number
    mäng_aktiivne = True
    mäng_lõppes_sõnum = ""
    praegune_tase_number = 1

    alusta_tase() # kutsume mängu alguses esimese taseme välja

# siit algab menüüga seotud definitsioonid
class Nupp():
    def __init__(self, x, y, tekst, font, funktsioon=None, üksvajutus=False):
        self.laius = 180
        self.kõrgus = 50
        self.funktsioon = funktsioon
        self.üksvajutus = üksvajutus
        self.juba_vajutatud = False
        self.olek = 'normal' 
        self.värvid = {'normal': "#4c3dcd", 'hover': "#8E8CFF"} # erinevad värvid eriseisundites
        self.rect = pygame.Rect(x, y, self.laius, self.kõrgus)
        self.pind = pygame.Surface((self.laius, self.kõrgus))
        self.teksti_pilt = font.render(tekst, True, (20, 20, 20))
        self.teksti_rect = self.teksti_pilt.get_rect(center=(self.laius // 2, self.kõrgus // 2))
        
    def joonista(self, aken):
        hiire_pos = pygame.mouse.get_pos() 
        # vaatame hiire positsiooni/tegevust ja vastavalt sellele muudame nupu värvi
        if self.rect.collidepoint(hiire_pos):
            self.olek = 'hover'
        else :
            self.olek = 'normal' 
            self.juba_vajutatud = False
        self.pind.fill(self.värvid[self.olek])
        self.pind.blit(self.teksti_pilt, self.teksti_rect)
        aken.blit(self.pind, self.rect)

    def käsitle_sündmus(self, sündmus):
        if sündmus.type == pygame.MOUSEBUTTONDOWN and sündmus.button == 1:       # kas hiir on nupu kohal
            if self.rect.collidepoint(sündmus.pos):
                    if self.funktsioon:
                        if self.üksvajutus and not self.juba_vajutatud:
                            self.funktsioon()
                            self.juba_vajutatud = True
                            return True
                        elif not self.üksvajutus:
                            self.funktsioon()
                            return True
        elif sündmus.type == pygame.MOUSEBUTTONUP and sündmus.button == 1:
            self.juba_vajutatud = False 
        return False
    

# menüü enda definitsioon
def menüü(aken, laius, mäng_lõppses_sõnum) :
    aken.fill(tumesinine)
    algus_funktsioon = alusta_mäng # anname def väärtusena, et oleks lihtsam välja kutsuda
    lõpp_funktsioon = sulge_mäng
    nupud = []
    joonista_tekst("Toida kass Mooritsat!", suur_font, kollane, 150) # tekst, näha menüül
    if mäng_lõppes_sõnum:
        # mis kuvatakse kui mäng on kaotatud
        joonista_tekst(mäng_lõppes_sõnum, väike_font, valge, 230)
        proovi_uuesti = Nupp(420, 360, 'Proovi uuesti', väike_font, algus_funktsioon, üksvajutus=True)
        välju = Nupp(420, 440, 'Välju', väike_font, lõpp_funktsioon, üksvajutus=True)
        nupud = [proovi_uuesti, välju]
    else:
        # mis kuvatakse mängu esialgsel avamisel
        joonista_tekst("Kogu kalu enne kui aeg otsa saab.", väike_font, valge, 230)
        alusta = Nupp(420, 360, 'Alusta', väike_font, algus_funktsioon, üksvajutus=True)
        välju = Nupp(420, 440, 'Välju', väike_font, lõpp_funktsioon, üksvajutus=True)
        nupud = [alusta, välju]
    for nupp in nupud :
        nupp.joonista(aken)
    return nupud

def vahekaart(aken) :
    global üleminek_millal, kas_vahekaart, mäng_aktiivne
    kaua_kestnud = pygame.time.get_ticks() - üleminek_millal
    kaua_kestab = 1600 # aeg on millisekundites
    aken.fill(tumesinine)
    joonista_tekst(f'Level {praegune_tase_number}', suur_font, punane, 280)
    if kaua_kestab <= kaua_kestnud :
        # vahekaart on kestnud ettenähtud aja, paneme oleku False'iks
        kas_vahekaart = False
        return True
    else :
        return False # vahekaardike veel kestab

class Kala:
    # defineerime kogutavad kalad
    def __init__(self, x, y):
        self.laius = 30
        self.kõrgus = 20
        self.rect = pygame.Rect(x, y, self.laius, self.kõrgus)

    def joonista(self, pind):
        pygame.draw.ellipse(pind, kollane, self.rect)  # keha
        saba = pygame.Rect(self.rect.right - 5, self.rect.centery - 8, 15, 16)  # saba 
        pygame.draw.polygon(
            pind,
            kollane,
            [
                (saba.left, saba.centery),
                (saba.right, saba.top),
                (saba.right, saba.bottom),
            ],
        )
        pygame.draw.circle(pind, must, (self.rect.left + 5, self.rect.centery - 3), 2)  # silm

def genereeri_kalad(kui_palju, platvormid):
    kalad = []
    katseid = 0
    miinimum_y = 80 # vaikimisi miinimum kõrgus
    if praegune_tase_number == 1:
        miinimum_y = 150
    while len(kalad) < kui_palju and katseid < kui_palju * 20:
        katseid += 1
        x = random.randint(50, laius - 80)
        y = random.randint(miinimum_y, kõrgus - 200)
        uus_rect = pygame.Rect(x, y, 30, 20)
        sobib = True
        # kontroll, et kala ei tekiks platvormi sisse
        for plat in platvormid:
            if uus_rect.colliderect(plat):
                sobib = False
                break
        if sobib:
            kalad.append(Kala(x,y))
    return kalad

# tasemega/leveliga seotud definitsioonid
class Tase :
    def __init__(self, aken, tase_number):
        self.aken = aken
        self.tase_number = tase_number
        self.taseme_info()
        self.platvormid = self.loo_platvormid(self.tase_number)
        self.kalad = genereeri_kalad(self.eesmärk + 3, self.platvormid)

    def taseme_info(self) :
        tase_number_kuvatav = self.tase_number - 1
        taseme_aeg_valem = 30 - tase_number_kuvatav * 3   # igal tasel on lühem ajalimiit, selle arvutamise valem
        if taseme_aeg_valem < 16 :
            self.taseme_aeg = 16 # taseme miinimum ajaks on 16 sekundit
        else :
            self.taseme_aeg = taseme_aeg_valem
        self.eesmärk = 5 + self.tase_number * 4  # iga tase kalade arvu valem

    def loo_platvormid(self, tase_number):
        platvormid = []
        maa = pygame.Rect(0, kõrgus - 80, laius, 100)  # maapind

        # kõrgemad platvormid, igal levelil on erinevad platvormid
        if tase_number == 1 :
            plat1 = pygame.Rect(100, 520, 200, 20)
            plat2 = pygame.Rect(400, 450, 250, 20)
            plat3 = pygame.Rect(750, 380, 200, 20)

        elif tase_number == 2 :
            plat1 = pygame.Rect(50, 450, 150, 20) 
            plat2 = pygame.Rect(300, 380, 200, 20)
            plat3 = pygame.Rect(650, 320, 150, 20)
            plat4 = pygame.Rect(800, 500, 100, 20) 
            platvormid.append(plat4)

        elif tase_number == 3 :
            plat1 = pygame.Rect(700, 480, 150, 20)
            plat2 = pygame.Rect(400, 360, 180, 20)
            plat3 = pygame.Rect(150, 280, 150, 20)
            plat4 = pygame.Rect(600, 200, 100, 20)
            platvormid.append(plat4)

        elif tase_number == 4 :
            plat1 = pygame.Rect(50, 400, 100, 20) 
            plat2 = pygame.Rect(200, 320, 100, 20)
            plat3 = pygame.Rect(450, 240, 120, 20)
            plat4 = pygame.Rect(650, 320, 100, 20) 
            plat5 = pygame.Rect(850, 400, 100, 20) 
            platvormid.append(plat4)
            platvormid.append(plat5)

        elif tase_number == 5 :
            plat1 = pygame.Rect(150, 480, 120, 20)
            plat2 = pygame.Rect(350, 380, 100, 20)
            plat3 = pygame.Rect(600, 280, 80, 20)
            plat4 = pygame.Rect(850, 200, 100, 20) 
            plat5 = pygame.Rect(50, 200, 100, 20) 
            platvormid.append(plat4)
            platvormid.append(plat5)

        platvormid += [plat1, plat2, plat3, maa]
        return platvormid


class Mängija(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))  
        self.image.fill(lilla)  
        self.rect = self.image.get_rect(topleft=(x, y))  # asukoht ekraanil
        self.kiirus_x = 0
        self.kiirus_y = 0
        self.liikumiskiirus = 6
        self.hüpe_jõud = -18  # kui kõrgele hüppab
        self.gravitatsioonijõud = 0.8  # kui kiiresti tagasi alla tuleb
        self.maas = False  # kas seisab platvormil või on õhus

    def sisend(self):
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_LEFT] or klahvid[pygame.K_a]:
            self.kiirus_x = -self.liikumiskiirus
        elif klahvid[pygame.K_RIGHT] or klahvid[pygame.K_d]:
            self.kiirus_x = self.liikumiskiirus
        else:
            self.kiirus_x = 0
        if klahvid[pygame.K_SPACE] and self.maas:
            self.kiirus_y = self.hüpe_jõud  # alustab hüpet

    def gravitatsioon(self, platvormid):
        # horisontaalne liikumine
        self.rect.x += self.kiirus_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > laius:
            self.rect.right = laius

        # vertikaalne liikumine (alla kukkumine)
        self.kiirus_y += self.gravitatsioonijõud
        if self.kiirus_y > 20:
            self.kiirus_y = 20
        self.rect.y += self.kiirus_y

        if self.rect.top < 0:  #ekraani piir
            self.rect.top = 0
            self.kiirus_y = 0

        # kontroll, kas on maa peal või platvormil
        self.maas = False
        for plat in platvormid:
            if self.rect.colliderect(plat):
                # mis toimub kui mängija läheneb ülevalt
                if self.kiirus_y > 0:
                    self.rect.bottom = plat.top # paneme ta platvormi peale
                    self.kiirus_y = 0
                    self.maas = True
                
                # mis toimub kui läheneme alt
                elif self.kiirus_y < 0:
                    self.rect.top = plat.bottom # topime ta alla
                    self.kiirus_y = 0

    def update(self, platvormid):
        self.sisend()
        self.gravitatsioon(platvormid)

def kuva_olek(pind, tase, kalu_kogutud, kalu_vaja, aeg_jäänud):
    """Kuvab taseme, kalade ja aja info."""
    tase_tekst = väike_font.render(f"Tase: {tase}/{max_tasemeid}", True, valge)
    pind.blit(tase_tekst, (20, 20))

    kala_tekst = väike_font.render(f"Kala: {kalu_kogutud}/{kalu_vaja}", True, valge)
    pind.blit(kala_tekst, (laius - 150, 20))

    aeg_tekst = väike_font.render(f"Aeg: {int(aeg_jäänud)} s", True, valge)
    pind.blit(aeg_tekst, (laius // 2 - 60, 20))

def kogu_kalad(mängija_rect, kalad, kalu_kogutud):
    """Kontrollib, kas mängija puutub kokku kaladega ja loendab need kokku."""
    alles = []
    lisandus = 0
    for kala in kalad:
        if mängija_rect.colliderect(kala.rect):
            lisandus += 1  
        else:
            alles.append(kala)
    return alles, kalu_kogutud + lisandus


# algsed seadistused enne mängu algust
mäng_aktiivne = False  # kas mäng on käimas või mitte
mäng_lõppes_sõnum = ""  # mida näidatakse, kui kaotad
praegused_nupud = menüü(aken, laius, mäng_lõppes_sõnum)
kas_vahekaart = False
mängija_grupp = pygame.sprite.GroupSingle()  
mängija_grupp.add(Mängija(100, kõrgus - 200))

while tsükkel:
    kell.tick(fps)
    for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                sulge_mäng()

            if not mäng_aktiivne and not kas_vahekaart:
                    for nupp in praegused_nupud :
                        nupp.käsitle_sündmus(sündmus)

    # peamine mängutsükkel, töötab siis kui vahekaarti pole ning mäng on aktiivne ja tase ka eksisteerib
    if mäng_aktiivne and praegune_tase and not kas_vahekaart:
        kalu_vaja = praegune_tase.eesmärk
        platvormid = praegune_tase.platvormid
        kalad = praegune_tase.kalad
        möödunud = (pygame.time.get_ticks() - tase_algus_aeg) / 1000.0
        aeg_jäänud = max(0, praegune_tase.taseme_aeg - möödunud)

        # uuendab mängijat ja kontrollib kalu
        mängija_grupp.update(praegune_tase.platvormid)
        mängija_sprite = mängija_grupp.sprite
        praegune_tase.kalad, kalu_kogutud = kogu_kalad(mängija_sprite.rect, kalad, kalu_kogutud)

        # kui tase läbitud
        if kalu_kogutud >= kalu_vaja:
            praegune_tase_number += 1
            if praegune_tase_number > max_tasemeid: # kas on läbitud piisavalt palju tasemeid, mäng lõppeb
                mäng_aktiivne = False
                mäng_lõppes_sõnum = "Sa toisid Mooritsa kõhu täis! Kõik tasemed läbitud."
            elif praegune_tase_number <= max_tasemeid : # kui ei ole piisavalt, siis laeb vahelehe sisse
                mäng_aktiivne = False
                kas_vahekaart = True
                üleminek_millal = pygame.time.get_ticks()

        # kui aeg otsas ja kalu puudu
        elif aeg_jäänud <= 0:
            mäng_aktiivne = False
            mäng_lõppes_sõnum = f"Moorits sõi su ära! Jõudsid tasemele {praegune_tase_number}."

        aken.fill(tumesinine) 

        for plat in platvormid:
            pygame.draw.rect(aken, hall, plat)

        for kala in praegune_tase.kalad:
            kala.joonista(aken)

        mängija_grupp.draw(aken)
        kuva_olek(aken, praegune_tase_number, kalu_kogutud, kalu_vaja, aeg_jäänud)
    
    elif not mäng_aktiivne and kas_vahekaart :
        if vahekaart(aken) :
            kas_vahekaart = False
            alusta_tase()
    else:
        praegused_nupud = menüü(aken, laius, mäng_lõppes_sõnum)
    pygame.display.flip()  