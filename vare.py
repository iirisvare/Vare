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
   • Pygame dokumentatsioon
   • Kursuse materjalid
   
Muu oluline info:
Projekti idee tuli päriselus olemasolevast kassist Mooritsast, kes on tugevalt toidulembeline ja vallatu.
Mängu eesmärk on pakkuda meelelahutust, peletada igavust ning panna proovile mängija kannatlikkus kasside suhtes.
"""
import pygame
import sys
import random

pygame.init()

laius = 900
kõrgus = 600
aken = pygame.display.set_mode((laius, kõrgus))  
pygame.display.set_caption("Projekt Vare")  
kell = pygame.time.Clock()  
fps = 60  

valge = (255, 255, 255)
must = (0, 0, 0)
hall = (60, 60, 60)
lilla = (180, 80, 200)
kollane = (255, 220, 80)
punane = (230, 50, 70)
tumesinine = (10, 15, 40)

suur_font = pygame.font.SysFont("bahnschrift", 52, True)  
väike_font = pygame.font.SysFont("bahnschrift", 24)  

max_tasemeid = 5  

def loo_platvormid():
    platvormid = []

    maa = pygame.Rect(0, kõrgus - 60, laius, 60)  # maapind
    platvormid.append(maa)

    # kõrgemad platvormid
    plat1 = pygame.Rect(150, 420, 180, 20)
    plat2 = pygame.Rect(550, 350, 200, 20)
    plat3 = pygame.Rect(350, 260, 140, 20)

    platvormid += [plat1, plat2, plat3]
    return platvormid

class Kala:

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
    while len(kalad) < kui_palju and katseid < kui_palju * 20:
        katseid += 1
        x = random.randint(50, laius - 80)
        y = random.randint(80, kõrgus - 150)
        uus_rect = pygame.Rect(x, y, 30, 20)
        sobib = True
        # kontroll, et kala ei tekiks platvormi sisse
        for plat in platvormid:
            if uus_rect.colliderect(plat):
                sobib = False
                break
        if sobib:
            kalad.append(Kala(x, y))
    return kalad

class Mängija(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))  
        self.image.fill(lilla)  
        self.rect = self.image.get_rect(topleft=(x, y))  # asukoht ekraanil
        self.kiirus_x = 0
        self.kiirus_y = 0
        self.liikumiskiirus = 6
        self.hüpe_jõud = -15  # kui kõrgele hüppab
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

        # kontroll, kas on maa peal või platvormil
        self.maas = False
        for plat in platvormid:
            if self.rect.colliderect(plat):
                if self.kiirus_y > 0 and self.rect.bottom >= plat.top:
                    self.rect.bottom = plat.top  # peatub platvormil
                    self.kiirus_y = 0
                    self.maas = True

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

def taseme_info(tase_indeks):
    """Annab iga taseme jaoks aja ja kalade arvu."""
    aeg = 25 - tase_indeks * 3  # iga tase lühem ajaliselt
    if aeg < 8:
        aeg = 8
    eesmärk = 5 + tase_indeks * 4  # iga tase rohkem kalu
    return {"aeg": aeg, "eesmärk": eesmärk}

mäng_aktiivne = False  # kas mäng on käimas või mitte
mäng_lõppes_sõnum = ""  # mida näidatakse, kui kaotad

praegune_tase = 1
kalu_kogutud = 0
kalu_vaja = 0
taseme_aeg = 0
taseme_algus_aeg = 0.0

platvormid = loo_platvormid()
kalad = []

mängija_grupp = pygame.sprite.GroupSingle()  
mängija_grupp.add(Mängija(100, kõrgus - 200))  

while True:
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not mäng_aktiivne:
            # kui mäng ei käi, saab tühikuga alustada uut
            if sündmus.type == pygame.KEYDOWN:
                if sündmus.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    # algväärtustamine uue mängu jaoks
                    mäng_aktiivne = True
                    mäng_lõppes_sõnum = ""
                    praegune_tase = 1
                    kalu_kogutud = 0

                    info = taseme_info(praegune_tase - 1)
                    taseme_aeg = info["aeg"]
                    kalu_vaja = info["eesmärk"]
                    taseme_algus_aeg = pygame.time.get_ticks()

                    platvormid = loo_platvormid()
                    kalad = genereeri_kalad(kalu_vaja + 3, platvormid)

                    mängija_grupp.empty()
                    mängija_grupp.add(Mängija(100, kõrgus - 200))

    if mäng_aktiivne:
        aeg = kell.tick(fps) / 1000.0
        möödunud = (pygame.time.get_ticks() - taseme_algus_aeg) / 1000.0
        aeg_jäänud = max(0, taseme_aeg - möödunud)

        # uuendab mängijat ja kontrollib kalu
        mängija_grupp.update(platvormid)
        mängija_sprite = mängija_grupp.sprite
        kalad, kalu_kogutud = kogu_kalad(mängija_sprite.rect, kalad, kalu_kogutud)

        # kui tase läbitud
        if kalu_kogutud >= kalu_vaja:
            praegune_tase += 1
            if praegune_tase > max_tasemeid:
                mäng_aktiivne = False
                mäng_lõppes_sõnum = "Sa toisid Mooritsa kõhu täis! Kõik tasemed läbitud."
            else:
                info = taseme_info(praegune_tase - 1)
                taseme_aeg = info["aeg"]
                kalu_vaja = info["eesmärk"]
                kalu_kogutud = 0
                taseme_algus_aeg = pygame.time.get_ticks()
                kalad = genereeri_kalad(kalu_vaja + 3, platvormid)

        # kui aeg otsas ja kalu puudu
        elif aeg_jäänud <= 0:
            mäng_aktiivne = False
            mäng_lõppes_sõnum = f"Moorits sõi su ära! Jõudsid tasemele {praegune_tase}."

        aken.fill(tumesinine)  # joonistamine

        for plat in platvormid:
            pygame.draw.rect(aken, hall, plat)

        for kala in kalad:
            kala.joonista(aken)

        mängija_grupp.draw(aken)
        kuva_olek(aken, praegune_tase, kalu_kogutud, kalu_vaja, aeg_jäänud)

    else:
        # menüü
        kell.tick(fps)
        aken.fill(tumesinine)

        def joonista_tekst(tekst, font, värv, y):
            pilt = font.render(tekst, True, värv)
            rect = pilt.get_rect(center=(laius // 2, y))
            aken.blit(pilt, rect)

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