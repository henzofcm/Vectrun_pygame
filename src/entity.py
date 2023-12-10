import pygame
from abc import ABCMeta


class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    """
    Base class for game entities.

    This class inherits from pygame.sprite.Sprite and serves as a base class for all game entities.
    It provides common functionality such as loading and scaling images, as well as updating the entity's state.

    Attributes
    ----------
    image : pygame.Surface
        The image of the entity.
    rect : pygame.Rect
        The rectangular area occupied by the entity on the screen.

    Methods
    -------
    __init__(self, image_path, x_y, scale_size)
        Initialize the Entity object.
    update(self)
        Update the entity's state.
    """
    def __init__(self, image_path, x_y, scale_size):
        """
        Initialize the Entity object.

        Parameters
        ----------
        image_path : str
            The path to the image file.
        x_y : tuple
            The x and y coordinates of the entity's top-left corner.
        scale_size : tuple
            The width and height to scale the image.


        Returns
        -------
        None
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, scale_size)
        self.rect = self.image.get_rect(topleft=x_y)


    def update(self):
            """
            Update the entity's state.

            Returns
            -------
            None
                This method does not return anything.
            """
            pass
