from livewires import games, color
import random

games.init(screen_width = 640, screen_height = 480, fps = 50)


class Pan(games.Sprite):
	image = games.load_image("pan.bmp")
	score = 0
	scoreChange = 0
	buffer = 0
	def __init__(self):
		super(Pan, self).__init__(image = Pan.image,
								  x = games.mouse.x,
								  bottom = games.screen.height)
		
		self.score = games.Text(value = 0, size = 25, color = color.black,
								top = 5, right = games.screen.width - 10)
		games.screen.add(self.score)

	def update(self):
		self.x = games.mouse.x
		
		if self.left < 0:
			self.left = 0
			
		if self.right > games.screen.width:
			self.right = games.screen.width

		if games.keyboard.is_pressed(games.K_1):
			Pizza.speed = .6
			Chef.speed = 2
		if games.keyboard.is_pressed(games.K_2):
			Pizza.speed = 1.1
			Chef.speed = 2.5
		if games.keyboard.is_pressed(games.K_3):
			Pizza.speed = 1.6
			Chef.speed = 3
		if games.keyboard.is_pressed(games.K_4):
			Pizza.speed = 2.1
			Chef.speed = 3.5
		if games.keyboard.is_pressed(games.K_5):
			Pizza.speed = 2.6
			Chef.speed = 4
		if games.keyboard.is_pressed(games.K_6):
			Pizza.speed = 3.1
			Chef.speed = 4.5
		if games.keyboard.is_pressed(games.K_7):
			Pizza.speed = 3.6
			Chef.speed = 5
		if games.keyboard.is_pressed(games.K_8):
			Pizza.speed = 4.1
			Chef.speed = 5.5
		if games.keyboard.is_pressed(games.K_9):
			Pizza.speed = 4.6
			Chef.speed = 6
			
		self.check_catch()

	def check_catch(self):
		for item in self.overlapping_sprites:		
			if(item.typeOf == "poison_pizza"):
				self.score.value -= 10
				Pan.score -= 10
				Pan.scoreChange -= 10
				self.score.right = games.screen.width - 10 
				item.handle_caught()
			elif(item.typeOf == "pineapple"):
				item.handle_caught()
			else:
				self.score.value += 10
				Pan.score += 10
				Pan.scoreChange += 10
				if(Pan.scoreChange % 500 == 0 and Pan.scoreChange > 0):
					Pan.buffer = 1
				self.score.right = games.screen.width - 10 
				item.handle_caught()

class Pizza(games.Sprite):
	image = games.load_image("pizza.bmp")
	speed = .6
	typeOf = "pizza"
	catch_sound = games.load_sound("explosion.wav")

	def __init__(self, x, y = 90):
		super(Pizza, self).__init__(image = Pizza.image,
									x = x, y = y,
									dy = Pizza.speed)

	def update(self):
		if self.bottom > games.screen.height:
			self.end_game()
			self.destroy()

	def handle_caught(self):
		self.destroy()
		self.catch_sound.play()
		

	def end_game(self):
		end_message = games.Message(value = "Game Over",
									size = 90,
									color = color.red,
									x = games.screen.width/2,
									y = games.screen.height/2,
									lifetime = 5 * games.screen.fps,
									after_death = games.screen.quit)
		games.screen.add(end_message)


class PoisonPizza(games.Sprite):
	image = games.load_image("poison_pizza.bmp")
	speed = .6
	typeOf = "poison_pizza"

	def __init__(self, x, y = 90):
		super(PoisonPizza, self).__init__(image = PoisonPizza.image,
									x = x, y = y,
									dy = Pizza.speed)

	def update(self):
		if self.bottom > games.screen.height:
			self.destroy()

	def handle_caught(self):
		self.destroy()
		Pizza.catch_sound.play()
		

class Pineapple(games.Sprite):
	image = games.load_image("pineapple.bmp")
	speed = .6
	typeOf = "pineapple"

	def __init__(self, x, y = 90):
		super(Pineapple, self).__init__(image = Pineapple.image,
									x = x, y = y,
									dy = Pizza.speed)

	def update(self):
		if self.bottom > games.screen.height:
			self.destroy()

	def handle_caught(self):
		self.destroy()
		end_message = games.Message(value = "Game Over",
									size = 90,
									color = color.red,
									x = games.screen.width/2,
									y = games.screen.height/2,
									lifetime = 5 * games.screen.fps,
									after_death = games.screen.quit)
		games.screen.add(end_message)

		
class Chef(games.Sprite):
	image = games.load_image("chef.bmp")

	def __init__(self, y = 55, speed = 2, odds_change = 200):
		image = games.load_image("chef.bmp")

	def __init__(self, y = 55, speed = 2, odds_change = 200):
		super(Chef, self).__init__(image = Chef.image,
								   x = games.screen.width / 2,
								   y = y,
								   dx = speed)
		
		self.odds_change = odds_change
		self.time_til_drop = 0

	def update(self):
		if self.left < 0 or self.right > games.screen.width:
			self.dx = -self.dx
		elif random.randrange(self.odds_change) == 0:
		   self.dx = -self.dx
				
		self.check_drop()


	def check_drop(self):
		if(Pan.score > 0 and Pan.score % 500 == 0 and Pan.buffer == 1):
			Pizza.speed += .2
			self.time_til_drop += 300
			Pan.buffer = 0
			Pan.scoreChange = 0
		if(self.time_til_drop > 0):
			self.time_til_drop -= 1
		else:

			randomNumber = random.randint(0,2)
			if(randomNumber == 0):
				new_object = Pizza(x = self.x)
			elif(randomNumber == 1):
				new_object = Pineapple(x = self.x)
			else:
				new_object = PoisonPizza(x = self.x) 
			games.screen.add(new_object)

			self.time_til_drop = int(new_object.height * 1.3 / Pizza.speed) + 1
			


def main():
	wall_image = games.load_image("wall.jpg", transparent = False)
	games.screen.background = wall_image
	the_chef = Chef()
	games.screen.add(the_chef)
	the_pan = Pan()
	games.screen.add(the_pan)
	games.mouse.is_visible = False
	games.screen.event_grab = False
	games.screen.mainloop()

main()
