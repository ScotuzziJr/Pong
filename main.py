import pygame, sys, random

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main window
width = 1020
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# Game elements
ball = pygame.Rect((width / 2) - 10, (height / 2) - 10, 20, 20)
player = pygame.Rect(10, (height / 2) - 70, 10, 140)
opponent = pygame.Rect((width - 20), (height / 2) - 70, 10, 140)
elementsColor = (200, 200, 200)
ballSpeedX = 5 * random.choice((1, -1))
ballSpeedY = 5 * random.choice((1, -1))
playerSpeed = 0
opponentSpeed = 7

# Scores
playerScore = 0
opponentScore = 0
gameFont = pygame.font.SysFont('consolas', 32)
scoreTime = True

# Sounds
gameSound = pygame.mixer.Sound('pong.ogg')
scoreSound = pygame.mixer.Sound('score.ogg')

while True:
	# Handles input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				playerSpeed += 7
			if event.key == pygame.K_UP:
				playerSpeed -= 7

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				playerSpeed -= 7
			if event.key == pygame.K_UP:
				playerSpeed += 7

	player.y += playerSpeed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= height:
		player.bottom = height

	if opponent.top < ball.y + 10:
		opponent.top += opponentSpeed
	if opponent.bottom > ball.y + 10:
		opponent.bottom -= opponentSpeed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= height:
		opponent.bottom = height

	# Animation
	ball.x += ballSpeedX
	ball.y += ballSpeedY

	if ball.top <= 0 or ball.bottom >= height:
		pygame.mixer.Sound.play(gameSound)
		ballSpeedY *= -1
	
	if ball.right >= width:
		pygame.mixer.Sound.play(scoreSound)
		playerScore += 1
		ball.center = ((width / 2), (height / 2))
		ballSpeedX *= random.choice((1, -1))
		ballSpeedY *= random.choice((1, -1))
		scoreTime = pygame.time.get_ticks()

	if ball.left <= 0:
		pygame.mixer.Sound.play(scoreSound)
		opponentScore += 1
		ball.center = ((width / 2), (height / 2))
		ballSpeedX *= random.choice((1, -1))
		ballSpeedY *= random.choice((1, -1))
		scoreTime = pygame.time.get_ticks()

	if (ball.colliderect(player)) and (ballSpeedX < 0):
		pygame.mixer.Sound.play(gameSound) 
		if abs(ball.left - player.right) < 10:
			ballSpeedX *= -1
		elif (abs(ball.bottom - player.top) < 10) and (ballSpeedY > 0):
			ballSpeedY *= -1
		elif (abs(ball.top - player.bottom) < 10) and (ballSpeedX < 0):
			ballSpeedY *= -1

	if (ball.colliderect(opponent)) and (ballSpeedX > 0):
		pygame.mixer.Sound.play(gameSound)
		if abs(ball.right - opponent.left) < 10:
			ballSpeedX *= -1
		elif (abs(ball.bottom - opponent.top) < 10) and (ballSpeedY > 0):
			ballSpeedY *= -1
		elif (abs(ball.top - opponent.bottom) < 10) and (ballSpeedX < 0):
			ballSpeedY *= -1

	# Visuals
	screen.fill(pygame.Color('grey12'))
	pygame.draw.rect(screen, elementsColor, player)
	pygame.draw.rect(screen, elementsColor, opponent)
	pygame.draw.rect(screen, elementsColor, ball)
	pygame.draw.aaline(screen, elementsColor, (width / 2, 100), (width / 2, height - 100))

	if scoreTime:
		currentTime = pygame.time.get_ticks()
		ball.center = ((width / 2), (height / 2))

		if currentTime - scoreTime < 700:
			numberThree = gameFont.render('3', False, elementsColor)
			screen.blit(numberThree, (500, 50))
		if 700 < currentTime - scoreTime < 1400:
			numberTwo = gameFont.render('2', False, elementsColor)
			screen.blit(numberTwo, (500, 50))
		if 1400 < currentTime - scoreTime < 2100:
			numberOne = gameFont.render('1', False, elementsColor)
			screen.blit(numberOne, (500, 50))

		if currentTime - scoreTime < 2100:
			ballSpeedX, ballSpeedY = 0, 0
		else:
			ballSpeedX = 5 * random.choice((1, -1))
			ballSpeedY = 5 * random.choice((1, -1))
			scoreTime = None

	playerText = gameFont.render(f'{playerScore}', False, elementsColor)
	screen.blit(playerText, (450, 350))

	opponentText = gameFont.render(f'{opponentScore}', False, elementsColor)
	screen.blit(opponentText, (550, 350))

	# Uptade the window
	pygame.display.flip()
	clock.tick(60)
