import pygame, sys
from maze import Maze
from player import Player
from game import Game
from clock import Clock
from button import Button

pygame.init()
pygame.font.init()
class Main():
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("impact", 30)
		self.message_color = pygame.Color("cyan")
		self.running = True
		self.game_over = False
		self.FPS = pygame.time.Clock()

	def instructions(self):
		instructions1 = self.font.render('Use', True, self.message_color)
		instructions2 = self.font.render('Arrow Keys', True, self.message_color)
		instructions3 = self.font.render('to Move', True, self.message_color)
		instructions4 = self.font.render('Up ↑',True,self.message_color)
		instructions5 = self.font.render('Down ↓ ',True,self.message_color)
		instructions6 = self.font.render('Right →',True,self.message_color)
		instructions7 = self.font.render('Left ←' ,True,self.message_color)
		self.screen.blit(instructions1,(655,300))
		self.screen.blit(instructions2,(610,331))
		self.screen.blit(instructions3,(630,362))
		self.screen.blit(instructions4,(630,400))
		self.screen.blit(instructions5,(630,430))
		self.screen.blit(instructions6,(630,460))
		self.screen.blit(instructions7,(630,490))
		
		
		

	# draws all configs; maze, player, instructions, and time
	def _draw(self, maze, tile, player, game, clock):
		# draw maze
		[cell.draw(self.screen, tile) for cell in maze.grid_cells]

		# add a goal point to reach
		game.add_goal_point(self.screen)

		# draw every player movement
		player.draw(self.screen)
		player.update()
		
		# instructions, clock, winning message
		self.instructions()
		if self.game_over:
			clock.stop_timer()
			self.screen.blit(game.message(),(610,120))
			pygame.time.wait(5000)
			pygame.display.set_mode((1280, 720))
			main_menu()
		else:
			clock.update_timer()
		self.screen.blit(clock.display_timer(), (625,200))
	
		pygame.display.flip()

	# main game loop
	def main(self, frame_size, tile):
		cols, rows = frame_size[0] // tile, frame_size[-1] // tile
		maze = Maze(cols, rows)
		game = Game(maze.grid_cells[-1], tile)
		player = Player(tile // 3, tile // 3)
		clock = Clock()

		maze.generate_maze()
		clock.start_timer()
		while self.running:
			self.screen.fill("gray")
			self.screen.fill( pygame.Color("darkslategray"), (603, 0, 752, 752))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			# if keys were pressed still
			if event.type == pygame.KEYDOWN:
				if not self.game_over:
					if event.key == pygame.K_LEFT:
						player.left_pressed = True
					if event.key == pygame.K_RIGHT:
						player.right_pressed = True
					if event.key == pygame.K_UP:
						player.up_pressed = True
					if event.key == pygame.K_DOWN:
						player.down_pressed = True
					player.check_move(tile, maze.grid_cells, maze.thickness)
		
			# if pressed key released
			if event.type == pygame.KEYUP:
				if not self.game_over:
					if event.key == pygame.K_LEFT:
						player.left_pressed = False
					if event.key == pygame.K_RIGHT:
						player.right_pressed = False
					if event.key == pygame.K_UP:
						player.up_pressed = False
					if event.key == pygame.K_DOWN:
						player.down_pressed = False
					player.check_move(tile, maze.grid_cells, maze.thickness)

			if game.is_game_over(player):
				self.game_over = True
				player.left_pressed = False
				player.right_pressed = False
				player.up_pressed = False
				player.down_pressed = False
				

			self._draw(maze, tile, player, game, clock)
			self.FPS.tick(60)
		
		

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Maze Game")

BG = pygame.image.load("Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                  Main(pygame.display.set_mode((752,602))).main((602,602),30)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()