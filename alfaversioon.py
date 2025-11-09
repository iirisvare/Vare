"""
Projekti teema:
Mäng, kus mängija peab kindla aja jooksul koguma etteantud arvu kalu.
Kui mängija jõuab vajaliku tulemuseni, avaneb järgmine level vähem
aja ja suurema kalade arvuga. Kui mängija ei saavuta eesmärki,
sööb kass Moorits mängija ära.

Autorid:
   • Ellinor Usai
   • Iiris Vare

Eeskujuna kasutatud allikad:
   • Pygame dokumentatsioon
   • Kursuse materjalid
   
Muu oluline info:
Projekti idee tuli päriselus olemasolevast kass Mooritsast, kes on
toidulembene ja vallatu. Mängu eesmärk on pakkuda meelelahutust,
lahendada igavuse probleemi ning mõõta pingetaluvust kasside suhtes.
"""

import pygame
from sys import exit

pygame.init()

# Ekraan
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Projekt Vare')
clock = pygame.time.Clock()

class PlayerRectangle(pygame.sprite.Sprite):
    """
    pygame.sprite.Sprite klassi pärimine.
    Sprite kasutamine võimaldab objektil töötada sprite-gruppidega, kasutada
    .update() ja .draw() meetodeid ning lisada hiljem mängu teisi objekte,
    ilma et kood muutuks segaseks.
    """
    
    # pygame.sprite.Sprite algseadistuse kutsumine, et objekt töötaks
    def __init__(self):
        super().__init__()

        # Ristkülik
        self.image = pygame.Surface((80, 150))  
        self.image.fill('white')

        # Ristküliku ekraani keskele panemine
        self.rect = self.image.get_rect(center=(400, 200))

        # Liikumiskiirus
        self.move_speed = 6

    # Klaviatuuri oleku lugemine ja ristküliku liigutamine vasakule/paremale
    def handle_keyboard_input(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.move_speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.move_speed

    # Mängija ekraanil püsimine
    def keep_inside_screen(self):
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

    def update(self):
        # Klahvide lugemine
        self.handle_keyboard_input()

        # Mängija ekraanil püsimise kontroll
        self.keep_inside_screen()

# Sprite-grupi loomine
player_group = pygame.sprite.GroupSingle()
player_group.add(PlayerRectangle())

# Mängu põhitsükkel 
while True:
    # Sündmused (akna sulgemine)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Ekraani puhastamine
    screen.fill('black')

    # Mängija uuendamine ja joonistamine
    player_group.update()
    player_group.draw(screen)

    # Kaadri ekraanile kuvamine
    pygame.display.update()

    # 60 kaadriga piiramine sekundis
    clock.tick(60)
