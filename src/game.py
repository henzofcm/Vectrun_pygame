import pygame
import sys

import entity
import rider
import utilities

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

        # Atributos para o estado do jogo
        self._game_turn = 0
        self._mov_stage = -1
        self._clicked = False

        # Cria o deck e a carta de seleção
        self._deck = deck
        self._selected_card = None

        # Cria o jogador
        self._player = rider.Player(1, (WIDTH / 2 - 1, GRID_Y / 2 - 2), (RIDER_X, RIDER_Y), self._deck)

        # Cria os bots
        __bot_list = []

        for bot in range(bot_number):
            __bot_list.append(rider.Bot(bot + 2, (WIDTH / 2 - 1, GRID_Y / 2 - 2), (RIDER_X, RIDER_Y), self._deck))

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
                if event.button == 1 and not self._clicked:
                    self.validate_click()

            # Animações de movimento
            for rider in self._all_riders:
                if event.type == rider.clock:
                    rider.update()

        # Verifica se sobrou apenas um, que será o vencedor
        if len(self._all_riders) == 1:
            # E então retorna o código do menu win ou lose
            if self._all_riders.sprites()[0]._number == 1:
                return 5
            else:
                return 6

        # Se tiver clicado, roda o movimento do jogador ou dos bots e testa colisão
        if self._clicked and self._all_riders:
            rider = self._all_riders.sprites()[self._mov_stage]

            # Só movimenta se o jogador estiver vivo
            if rider.state_alive:
                self.move_player(rider)
                self.check_collision(rider)

        # Verifica se alguém morreu e roda sua animação
        for rider in self._all_riders:
            if not rider.state_alive:
                # Quando acabar continua a rodada
                if rider.update_death():
                    self.__end_death()

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
        # Desenha o tabuleiro no layer mais baixo
        screen.blit(self.image, self.rect)

        # Desenha as linhas dos riders
        for rider in self._all_riders.sprites():
            pygame.draw.lines(screen, rider._color, False, rider._path + [rider.rect.center], width=6)

        # Desenha a carta selecionada, caso exista
        if self._selected_card:
            self._selected_card.draw(screen)

        # Desenha o contorno e as cartas
        for rider in self._all_riders:
            self.choice_preview(screen, rider)
            rider._hand.draw(screen)

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
                if self._selected_card.sprites()[0].rect.center == player_card.rect.center:
                    self._clicked = True
                    self.sound[3].play()
                    self.next_turn(player_card)

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
        
    def __end_death(self):
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
                    card.image = pygame.transform.rotate(card.image, -90)
                elif rider._number == 2:
                    card.image = pygame.transform.rotate(card.image, -270)
                elif rider._number == 4:
                    card.image = pygame.transform.rotate(card.image, -180)
