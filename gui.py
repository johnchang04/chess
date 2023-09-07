import pygame
from chess.chess_project_logic import *

b = GameBoard()
white, black = b.white, b.black
img_dictionary = {Pawn: u'\u265f', Knight: u'\u265e', Bishop: u'\u265d', Rook: u'\u265c', Queen: u'\u265b', King: u'\u265a'}

def select(square):
    player = b.turn
    if player.held:
        Player.move(player, player.held.coords, square)

    else:
        piece = b.squares[square]
        if piece and piece.color == player.color:
            player.held = piece

pygame.init()
margin = 35

screen = pygame.display.set_mode((640+(margin*2), 640+(margin*2)))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

squares_array = []


class Square(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
       pygame.sprite.Sprite.__init__(self)
       self.color = color
       self.coords = None
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.rect = self.image.get_rect()


running = True

screen.fill("brown4")

for x in range(8):
    for y in range(8):
        x0, y0 = x * 80, y * 80
        color = 'medium blue'
        if (x + y) % 2 == 0:
            color = 'gold3'
        sq = Square(color, 80, 80)
        sq.rect = sq.image.get_rect(topleft=(x0+margin, y0+margin))
        sq.coords = convert(x+1, y+1)
        sq.piece_img = None
        pygame.draw.rect(screen, color, sq.rect)
        squares_array.append(sq)
pygame.font.init()

def place_piece_img(sqr, unistr, color):
    text_surface_object = pygame.font.Font("FreeSerif.ttf", 75).render(unistr, True, color)
    text_rect = text_surface_object.get_rect(center=sqr.rect.center)
    screen.blit(text_surface_object, text_rect)
    sqr.piece_img = unistr


def setup_piece_imgs(sqr):
        if "2" in sqr.coords:
            place_piece_img(sqr, img_dictionary[Pawn], 'white')
            return
        if "7" in sqr.coords:
            place_piece_img(sqr, img_dictionary[Pawn], 'black')
            return
        if sqr.coords in ['a1', 'h1']:
            place_piece_img(sqr, img_dictionary[Rook], 'white')
            return
        if sqr.coords in ['a8', 'h8']:
            place_piece_img(sqr, img_dictionary[Rook], 'black')
            return
        if sqr.coords in ["b1", "g1"]:
            place_piece_img(sqr, img_dictionary[Knight], 'white')
            return
        if sqr.coords in ["b8", "g8"]:
            place_piece_img(sqr, img_dictionary[Knight], 'black')
            return
        if sqr.coords in ['c1', 'f1']:
            place_piece_img(sqr, img_dictionary[Bishop], 'white')
            return
        if sqr.coords in ['c8', 'f8']:
            place_piece_img(sqr, img_dictionary[Bishop], 'black')
            return
        if sqr.coords == 'd1':
            place_piece_img(sqr, img_dictionary[Queen], 'white')
            return
        if sqr.coords == 'd8':
            place_piece_img(sqr, img_dictionary[Queen], 'black')
            return
        if sqr.coords == 'e1':
            place_piece_img(sqr, img_dictionary[King], 'white')
            return
        if sqr.coords == 'e8':
            place_piece_img(sqr, img_dictionary[King], 'black')
            return


for sqr in squares_array:
    setup_piece_imgs(sqr)


def find_sprite(board_coords):
    for sqrite in squares_array:
        if sqrite.coords == board_coords:
            return sqrite


while running:

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_player = b.turn
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in squares_array if s.rect.collidepoint(pos)]

            for sprite in clicked_sprites:
                pygame.draw.rect(screen, 'dark green', sprite.rect)
                clicked_piece = b.squares[sprite.coords]
                held_piece = current_player.held

                if held_piece:
                    if clicked_piece and clicked_piece.color == current_player.color:
                        place_piece_img(sprite, sprite.piece_img, clicked_piece.color)
                        current_player.held = clicked_piece

                    else:
                        old_square = find_sprite(held_piece.coords)
                        track_move = current_player.move(held_piece.coords, sprite.coords)
                        if not b.squares[held_piece.coords]:
                            held_piece_img = find_sprite(held_piece.coords).piece_img

                            place_piece_img(sprite, held_piece_img, held_piece.color)
                            pygame.draw.rect(screen, old_square.color, old_square.rect)

                            sprite.piece_img = held_piece_img
                            old_square.piece_img = None

                            if track_move == 'Castle':
                                if '1' in sprite.coords:
                                    rook_row = '1'
                                else:
                                    rook_row = '8'

                                if 'c' in sprite.coords:
                                    rook_old = find_sprite('a' + rook_row)
                                    rook_new = find_sprite('d' + rook_row)
                                elif 'g' in sprite.coords:
                                    rook_old = find_sprite('h' + rook_row)
                                    rook_new = find_sprite('f' + rook_row)

                                rook_old_img = rook_old.piece_img

                                place_piece_img(rook_new, rook_old_img, held_piece.color)
                                rook_new.img = rook_old_img

                                pygame.draw.rect(screen, rook_old.color, rook_old.rect)
                                rook_old.img = None

                else:
                    if sprite.piece_img:
                        place_piece_img(sprite, sprite.piece_img, clicked_piece.color)

                    if clicked_piece and clicked_piece.color == current_player.color:
                        current_player.held = clicked_piece

                pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONUP:
            current_player = b.turn.opp
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in squares_array if s.rect.collidepoint(pos)]

            for sprite in clicked_sprites:
                pygame.draw.rect(screen, sprite.color, sprite.rect)
                clicked_piece = b.squares[sprite.coords]

                if clicked_piece:
                    place_piece_img(sprite, sprite.piece_img, clicked_piece.color)
                pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()





