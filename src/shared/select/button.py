from ...enums import ButtonTypeEnum, ButtonSizeEnum

from .. import Button


class SelectButton(Button):
    def __init__(
        self,
        x,
        y,
        content,
        type=ButtonTypeEnum.PRIMARY,
        size=ButtonSizeEnum.MEDIUM,
    ):
        super().__init__(x, y, content, type, size)

        self.set_local_config()

        self.width = self.config["width"]
        self.height = self.config["height"]
        self.fontsize = self.config["fontsize"]

        self.set_content()
        self.set_button_image()

        self.blit_button()

    def set_local_config(self):
        self.config["width"] = 46
        self.config["height"] = 46
        self.config["fontsize"] = 36

        if self.size == ButtonSizeEnum.SMALL:
            self.config["width"] = 36
            self.config["height"] = 36
            self.config["fontsize"] = 32

        if self.size == ButtonSizeEnum.LARGE:
            self.config["width"] = 52
            self.config["height"] = 52
            self.config["fontsize"] = 50

    def set_button_image(self):
        self.image = self.create_overlay()
        self.image.fill(self.config["color"])
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
