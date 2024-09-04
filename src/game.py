import pygame
import sys
import pickle

import entity
import rider
import utilities
from menu import Button

from deck import *
from config import *


class GridGame(entity.Entity):
    """
    Represents the grid game.
    
    This class inherits from Entity and represents the grid game.
    It is responsible for handling the game's main events, such as quitting the game,
    pressing the escape key, and clicking the mouse button. If a click occurs,
    it validates the click and performs the player's movement and collision testing.
    
    Attributes
    ----------
    image_path : str
        The path to the image file.
    x_y : tuple
        The x and y coordinates of the game object.
    scale_size : float
        The scale size of the game object.
    bot_number : int
        The number of bots in the game.
    _game_turn : int
        The current turn of the game.
    _mov_stage : int
        The current stage of the player's movement.
    _clicked : bool
        True if the player has clicked, False otherwise.
    _deck : Deck
        The deck of cards.
    _player : Player
        The player object.
    _bots : Group
        The group of bots.
    _all_riders : Group
        The group of all riders.
        
    Methods
    -------
    __init__(self, image_path, x_y, scale_size, bot_number)
        Initializes the Game object.
    update(self)
        Update the game state.
    draw(self, screen)
        Draw the game elements on the screen.
    choice_preview(self, screen)
        Preview the selected card and its path on the screen.
    __preview_selected_card(card, screen)
        Draw the outline of the selected card.
    __preview_selected_path(card, screen)
        Preview the selected path on the screen.
    validate_click(self)
        Verifies if the player clicked on a card and prepares the player's movement.
    __card_clicked(self)
        Verifies if a card has been clicked by the player.
    move_player(self, rider)
        Move the player's rider.
    __end_turn(self)
        Reverses the game state and advances the turn.
    __next_player_movement(self, card=None)
        Perform the movement of the next player in the game.
    __first_turn_collision(self)
        Verifies if any rider has collided during the first turn.
    check_collision(self, rider)
        Check for collisions between the rider and the game elements.
    __kill_rider(self, rider)
        Kills the specified rider and advances the turn.
    """

    def __init__(self, image_path, x_y, scale_size, bot_number, volume, deck):
        """
        Initializes the Game object.

        Parameters
        ----------
        image_path : str
            The path to the image file.
        x_y : tuple
            The x and y coordinates of the game object.
        scale_size : float
            The scale size of the game object.
        bot_number : int
            The number of bots in the game.

        Returns
        -------
        None
        """
        super().__init__(image_path, x_y, scale_size)
        self.background = entity.Entity(TEXTURE_MENU_PATH + "background.png", (0, 0), (WIDTH, HEIGHT))
        self.table = entity.Entity(TEXTURE_PATH + "table_" + str(bot_number + 1) + ".png", (0, 0), (WIDTH, HEIGHT))
        self.border = entity.Entity(TEXTURE_PATH + "border.png", (0, 0), (WIDTH, HEIGHT))
        self.btn_back = Button(TEXTURE_MENU_PATH + "back_button.png", (WIDTH / 2, BUTTON_Y / 4), (BUTTON_Y * 2.6742 / 2, BUTTON_Y / 2), 1)

        # Lê o arquivo do score
        self.__win_list = pickle.load(open('score.pkl', 'rb'))

        # Carrega o botão de vitória e os de derrota
        self.__win = None

        self.__dead = [0, 0, 0, 0]
        self.__lose_group = pygame.sprite.OrderedUpdates()

        for x in range(4):
            if x == 0:
                lose_button = entity.Entity(TEXTURE_MENU_PATH + "lose_button.png", (WIDTH * 0.089 + CARD_Y, 3 * HEIGHT * 0.037 / 2 + CARD_X), (BUTTON_Y * 1.5564, BUTTON_Y))
                lose_button.image = pygame.transform.rotate(lose_button.image, 270)
            elif x == 1:
                lose_button = entity.Entity(TEXTURE_MENU_PATH + "lose_button.png", (WIDTH - 2 * CARD_Y - WIDTH * 0.089, 3 * HEIGHT * 0.037 / 2 + CARD_X), (BUTTON_Y * 1.5564, BUTTON_Y))
                lose_button.image = pygame.transform.rotate(lose_button.image, 90)
            elif x == 2:
                lose_button = entity.Entity(TEXTURE_MENU_PATH + "lose_button.png", (WIDTH * 0.089 + CARD_Y, HEIGHT * 0.537 + CARD_X), (BUTTON_Y * 1.5564, BUTTON_Y))
                lose_button.image = pygame.transform.rotate(lose_button.image, 270)
            elif x == 3:
                lose_button = entity.Entity(TEXTURE_MENU_PATH + "lose_button.png", (WIDTH - 2 * CARD_Y - WIDTH * 0.089, HEIGHT * 0.537 + CARD_X), (BUTTON_Y * 1.5564, BUTTON_Y))
                lose_button.image = pygame.transform.rotate(lose_button.image, 90)

            self.__lose_group.add(lose_button)

        # Atributos para o estado do jogo
        self._game_turn = 0
        self._mov_stage = -1
        self._clicked = False

        # Cria o deck e a carta de seleção
        self._deck = deck
        self._selected_card = None
        self._drawn_card = entity.Entity(TEXTURE_MENU_PATH + "foo.png", (0, 0), (32, 32))

        # Cria o jogador
        self._player = rider.Player(1, (WIDTH / 2, HEIGHT / 2), (RIDER_X, RIDER_Y), self._deck)

        # Cria os bots
        __bot_list = []

        for bot in range(bot_number):
            __bot_list.append(rider.Bot(bot + 2, (WIDTH / 2 , HEIGHT / 2), (RIDER_X, RIDER_Y), self._deck))

        self._bots = pygame.sprite.OrderedUpdates(__bot_list[::-1])

        # Grupo com todos personagens animados (bots e player)
        self._all_riders = pygame.sprite.OrderedUpdates((self._player.sprite()), self._bots.sprites()[::-1])

        # Carrega efeitos sonoros pra memória
        self.volume = volume * 3 / 4
        self.sound = []

        for index in range(SOUND_NUMBER):
            archive = "sound_" + str(index) + ".ogg"
            sound = pygame.mixer.Sound(SOUND_PATH + archive)
            sound.set_volume(self.volume / 2)
            self.sound.append(sound)

        # Cria um canal para tocar os efeitos sonoros
        self.channel = pygame.mixer.Channel(1)
        self.channel.set_volume(self.volume)

    def update(self):
        """
        Update the game state.

        This method handles the main events of the menu, such as quitting the game,
        pressing the escape key, and clicking the mouse button. If a click occurs,
        it validates the click and performs the player's movement and collision testing.

        Returns
        -------
        bool
            False.
        """
        # Eventos principais deste menu
        for event in pygame.event.get():
            # Caso feche
            if event.type == pygame.QUIT:
                self.channel.stop()
                pygame.quit()
                sys.exit()

            # ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.channel.stop()
                    return 1
                
            # Cliques
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Caso saia do jogo
                    if self.btn_back.update():
                        return 1
                    
                    # Caso clique em alguma carta
                    if not self._clicked:
                        self.validate_click()

            # Animações de movimento
            for rider in self._all_riders:
                if event.type == rider.clock:
                    rider.update()

        # Verifica se sobrou apenas um, que será o vencedor
        if len(self._all_riders) == 1 and not self.__win:
            self._clicked = True
            self.__win = entity.Entity(TEXTURE_MENU_PATH + "win_button.png", (WIDTH * 0.089 + CARD_Y, 3 * HEIGHT * 0.037 / 2 + CARD_X), (BUTTON_Y * 1.5564, BUTTON_Y))
            self.__win.image = pygame.transform.rotate(self.__win.image, 270)

            # E então altera o botão de quem ganhou
            if self._all_riders.sprites()[0]._number == 1:
                self.__win_list[0] += 1
            elif self._all_riders.sprites()[0]._number == 2:
                self.__win_list[1] += 1
                self.__win.rect.left = WIDTH - 2 * CARD_Y - WIDTH * 0.089
                self.__win.image = pygame.transform.rotate(self.__win.image, 180)
            elif self._all_riders.sprites()[0]._number == 3:
                self.__win_list[2] += 1
                self.__win.rect.top = HEIGHT * 0.537 + CARD_X
            elif self._all_riders.sprites()[0]._number == 4:
                self.__win_list[3] += 1
                self.__win.rect.left = WIDTH - 2 * CARD_Y - WIDTH * 0.089
                self.__win.rect.top = HEIGHT * 0.537 + CARD_X
                self.__win.image = pygame.transform.rotate(self.__win.image, 180)

            # Salva o score em um arquivo
            pickle.dump(self.__win_list, open('score.pkl', 'wb'))

        # Se tiver clicado, roda o movimento do jogador ou dos bots e testa colisão
        if self._clicked and self._all_riders and not self.__win:
            rider = self._all_riders.sprites()[self._mov_stage]

            # Só movimenta se o jogador estiver vivo
            if rider.state_alive:
                self.move_player(rider)
                self.check_collision(rider)

        # Verifica se alguém morreu e roda sua animação
        for rider in self._all_riders:
            if not rider.state_alive:
                # Quando acabar continua a rodada
                dead_num = rider.update_death()

                if dead_num:
                    self.__end_death(dead_num)

        return 0

    def draw(self, screen):
        """
        Draw the game elements on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the game elements on.

        Returns
        -------
            None
        """
        # Desenha o background, o tabuleiro e a mesa
        screen.blit(self.background.image, self.background.rect)
        screen.blit(self.image, self.rect)
        #screen.blit(self.border.image, self.border.rect)
        screen.blit(self.table.image, self.table.rect)
        screen.blit(self.btn_back.image, self.btn_back.rect)

        # Desenha as linhas dos riders
        for rider in self._all_riders.sprites():
            pygame.draw.lines(screen, rider._color, False, rider._path + [rider.rect.center], width=6)

        # Desenha a carta selecionada, caso exista
        if self._selected_card:
            self._selected_card.draw(screen)
            
            if self._clicked:
                screen.blit(self._drawn_card.image, self._drawn_card.rect)

        # Desenha o contorno e as cartas
        for rider in self._all_riders:
            self.choice_preview(screen, rider)
            rider._hand.draw(screen)

        # Caso alguém tenha morrido
        for idx, num in enumerate(self.__dead):
            if num:
                button = self.__lose_group.sprites()[idx]
                screen.blit(button.image, button.rect)

        # Caso alguém tenha ganho
        if self.__win:
            screen.blit(self.__win.image, self.__win.rect)

        # Faz blit no jogador e nos bots
        self._bots.draw(screen)
        self._player.draw(screen)

        # Se alguém estiver na animação de morte, desenha de acordo
        for rider in self._all_riders.sprites():
            if not rider.state_alive:
                screen.blit(rider.last_image, rider.last_rect)

    def choice_preview(self, screen, rider):
        """
        Preview the selected card and its path on the screen.

        Parameters
        ----------
            screen : pygame.Surface
            The screen surface to draw on.

        Returns
        -------
            None
        """
        # Verifica se o mouse está em cima da carta
        for card in rider._hand.sprites():
            if card.update():
                # Desenha o contorno
                self.__preview_selected_card(card, rider._color).draw(screen)

                # Se não houver clicado antes, mostra a trajetória da carta
                if not self._clicked:
                    self.__preview_selected_path(card, screen, rider)

    @staticmethod
    def __preview_selected_card(card, color):
        """
        Draw the outline of the selected card.

        Parameters
        ----------
        card : Card
            The selected card object.
        screen : pygame.Surface
            The screen surface to draw on.

        Returns
        -------
        None
        """
        # Desenha o contorno da carta selecionada
        rect_pos = (card.rect.left - CARD_SELECTED_WIDTH, card.rect.top - CARD_SELECTED_WIDTH)
        rect_size = (card.rect.width + 2 * CARD_SELECTED_WIDTH, card.rect.height + 2 * CARD_SELECTED_WIDTH)

        # Cria um rect e uma surf para o contorno
        rect = pygame.Rect(rect_pos, rect_size)
        surf = pygame.Surface(rect.size)
        surf.fill(color)

        # E retorna o sprite delas
        selection = pygame.sprite.Sprite()
        selection.image = surf
        selection.rect = rect

        return pygame.sprite.Group(selection)

    def __preview_selected_path(self, card, screen, rider):
        """
        Preview the selected path on the screen.

        Parameters
        ----------
        card : Card
            The selected card.
        screen : pygame.Surface
            The screen surface to draw on.

        Returns
        -------
        None
        """
        # Pega o ponto inicial e final da reta
        start = pygame.Vector2(rider._path[-1])  # Converte para Vector2
        card_value = pygame.Vector2(card.value[0], -card.value[1])

        size_segments = 12  # Defina a distância desejada entre os segmentos da linha tracejada
        num_segments = int(start.distance_to(start + card_value * DISTANCE) / size_segments)

        # Desenha a linha tracejada
        for i in range(0, num_segments, 2):
            segment_start = start + card_value * i * DISTANCE / num_segments
            segment_end = start + card_value * (i + 1) * DISTANCE / num_segments
            pygame.draw.line(screen, rider._color, segment_start, segment_end, width=5)
        
    def validate_click(self):
        """
        Verifies if the player clicked on a card and prepares the player's movement.

        Returns
        -------
            None
        """
        # Verifica em qual carta clicou
        player_card = self.__card_clicked()

        # Se tiver clicado, prepara o movimento do player ou seleciona a carta
        if player_card:
            if self._selected_card:
                # Se tiver escolhido a mesma carta que selecionou
                if self._selected_card.sprites()[0].rect.center == player_card.rect.center:
                    self._clicked = True
                    self.sound[3].play()
                    self.next_turn(player_card)

                    # Salva a imagem da carta clicada rotacionada
                    self._drawn_card.image = pygame.transform.rotozoom(player_card.image, 180, 1.2)
                    player_num = self._all_riders.sprites()[self._mov_stage]._number
                    
                    # E posiciona para que seja possível os demais jogadores verem
                    if player_num == 1:
                        self._drawn_card.rect.topleft = (WIDTH * 0.089 + CARD_Y, 3 * HEIGHT * 0.037 / 2 + CARD_X * 5 / 6)
                    elif player_num == 2:
                        self._drawn_card.rect.topleft = (WIDTH - 2 * CARD_Y * 1.2 - WIDTH * 0.089, 3 * HEIGHT * 0.037 / 2 + CARD_X * 5 / 6)
                    elif player_num == 3:
                        self._drawn_card.rect.topleft = (WIDTH * 0.089 + CARD_Y, HEIGHT * 0.537 + CARD_X * 5 / 6)
                    elif player_num == 4:
                        self._drawn_card.rect.topleft = (WIDTH - 2 * CARD_Y * 1.2 - WIDTH * 0.089, HEIGHT * 0.537 + CARD_X * 5 / 6)

                    return
            
            rider = self._all_riders.sprites()[self._mov_stage + 1]
            self._selected_card = self.__preview_selected_card(player_card, rider._color)

    def __card_clicked(self):
        """
        Verifies if a card has been clicked by the player.

        Returns
        -------
            Card or None: The clicked card if found, None otherwise.
        """

        rider = self._all_riders.sprites()[self._mov_stage + 1]
        
        # Se o jogador da vez clicar na carta, _clicked = True
        for card in rider._hand.sprites():
            if card.update():
                return card

        return None
            
    def move_player(self, rider):
        """
        Move the player's rider.

        Parameters
        ----------
        rider : Rider
            The rider object to be moved.

        Returns
        -------
            None

        Notes
        -----
        If the rider is able to update its position on the deck, nothing happens.
        If the rider is unable to update its position, the next player movement is reset.
        """
        # Move o rider
        if rider.move_rider(self._deck):
            return
        # Se ficou parado, reseta o movimento
        else:
            self.end_move()

    def __end_turn(self):
        """
        Reverses the game state and advances the turn.

        Returns
        -------
            None
        """
        # Só reverte o estado do jogo e adiciona um turno
        self._game_turn += 1
        self._clicked = False
        self._mov_stage = -1

    def next_turn(self, card):
        self._mov_stage += 1

        # Prepara o jogo para rodar mais uma animação
        next_player = self._all_riders.sprites()[self._mov_stage]

        # Atualiza o estado do próximo jogador
        next_player.select_card(card)

        # Toca o som de movimento indefinidamente
        self.channel.play(self.sound[1], -1)

    def end_move(self):
        self._clicked = False
        self._selected_card = None

        # Para o som do movimento
        self.channel.stop()

        # Se todos jogadores tiverem se movimentado, acaba o turno
        if self._mov_stage + 1 == len(self._all_riders):
            self.__end_turn()

            # No raro caso de colidirem no primeiro turno
            if self._game_turn == 1:
                self.__first_turn_collision()
    
        #Se todos morrerem também retorna
        if not self._all_riders:
            return

    def __first_turn_collision(self):
        """
        Verifies if any rider has collided during the first turn.

        This method checks if any rider has collided with the border or with other riders during the first turn of the game.
        If a collision is detected, the corresponding rider is removed from the game.

        Returns
        -------
            None
        """
        # Verifica se alguém colidiu no primeiro turno
        for rider in self._all_riders.sprites()[::-1]:
            # Testa apenas colisão com as linhas pois é impossivel colidir com fronteira
            if utilities.check_line_collision(self._all_riders, rider) and self._game_turn:
                rider.kill_rider()
                self.sound[0].play()
                continue

    def check_collision(self, rider):
        """
        Check for collisions between the rider and the game elements.

        Parameters
        ----------
            rider (Rider): The rider object to check for collisions.

        Returns
        -------
            None
        """
        # Testa colisão com a fronteira
        if utilities.check_border_collision(rider.rect.center):
            rider.kill_rider()
            self._selected_card = None
            self.sound[0].play()
            return

        # Verifica se colidiram entre si
        temp_group = self._all_riders.copy()
        temp_group.remove(rider)

        for enemy in temp_group:
            if utilities.check_riders_collision(rider, enemy) and self._game_turn:
                rider.kill_rider()
                enemy.kill_rider()
                self._selected_card = None
                self.sound[0].play()
                return

        # Testa colisão com as linhas
        if utilities.check_line_collision(self._all_riders, rider) and self._game_turn:
            rider.kill_rider()
            self._selected_card = None
            self.sound[0].play()
            return
        
    def __end_death(self, dead_num):
        # Atualiza a lista de mortos
        self.__dead[dead_num - 1] = 1
        
        # Termina a rodada se não houver mais nenhuma animação ocorrendo
        for rider in self._all_riders.sprites():
            if not rider.state_alive:
                # É possível o jogador atual matar um anterior (TODO)
                if rider._number < self._mov_stage + 1:
                    self._mov_stage -= 1
                
                return

        # Se todos que sobraram estiverem vivos, continua a partida
        self._mov_stage -= 1
        self.end_move()

    def close(self):
        # Desrotaciona as cartas
        for rider in self._all_riders:
            for card in rider._hand:
                if rider._number == 1:
                    card.image = pygame.transform.rotate(card.image, -270)
                elif rider._number == 2:
                    card.image = pygame.transform.rotate(card.image, -90)
                elif rider._number == 3:
                    card.image = pygame.transform.rotate(card.image, -270)
                elif rider._number == 4:
                    card.image = pygame.transform.rotate(card.image, -90)
