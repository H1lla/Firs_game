from random import randint

from superwires import games

games.init(screen_width=1382, screen_height=778, fps=50)
wall_image = games.load_image('1621333311_12-phonoteka_org-p-krasivii-fon-dlya-menyu-igri-12.jpg', transparent=False)
games.screen.background = wall_image

bin_image = games.load_image('Trach.jpg')


class BinSprite(games.Sprite):
    def __init__(self, x, type_name):
        self.type_name = type_name
        super(BinSprite, self).__init__(image=bin_image, x=x, y=650)

    def handle_click(self):
        if len(builder.visible_waste) > 0:
            lowest_waste = builder.visible_waste[0]
            if lowest_waste.type_name == self.type_name:
                builder.visible_waste.remove(lowest_waste)
                games.screen.remove(lowest_waste)

    def update(self):
        overlapping_sprites = self.get_overlapping_sprites()

        for sprite in overlapping_sprites:
            if sprite.type_name != self.type_name:
                games.screen.quit()


class WasteSprite(games.Sprite):
    def __init__(self, image, type_name):
        self.type_name = type_name
        super(WasteSprite, self).__init__(image=image, x=games.screen.width / 2,
                                          y=games.screen.height - 817,
                                          dx=0,
                                          dy=2)


class WasteBuilderSprite(games.Sprite):
    def __init__(self):
        self.in_removal_mode = False
        self.click_was_handled = False
        self.frames_interval = 60
        self.passed_frame = 0
        self.create_waste = 0
        self.visible_waste = []
        super(WasteBuilderSprite, self).__init__(image=bin_image, x=-200, y=-200)

    def update(self):
        if self.passed_frame == 0:
            self.create_waste += 1
            new_waste = random_waste()
            self.visible_waste.append(new_waste)
            games.screen.add(new_waste)

        self.passed_frame += 1

        if self.passed_frame == self.frames_interval:
            self.passed_frame = 0

        if self.create_waste == 20:
            self.frames_interval = 45
        elif self.create_waste == 40:
            self.frames_interval == 30
        elif self.create_waste == 60:
            self.frames_interval = 20

        if games.mouse.is_pressed(0):
            if self.in_removal_mode is False:
                self.in_removal_mode = True
                self.click_was_handled = False

        elif self.click_was_handled:
            self.in_removal_mode = False

        if self.in_removal_mode and self.click_was_handled is False:
            if check_point(games.mouse.x, games.mouse.y, bin_orange):
                bin_orange.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bin_bottle):
                bin_bottle.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bin_paper):
                bin_paper.handle_click()

            self.click_was_handled = True


bin_orange = BinSprite(x=160, type_name='orange')
bin_bottle = BinSprite(x=680, type_name='bottle')
bin_paper = BinSprite(x=1220, type_name='paper')

builder = WasteBuilderSprite()


def check_point(x, y, sprite):
    return sprite.left <= x <= sprite.right and sprite.top <= y <= sprite.bottom


def random_waste():
    value = randint(1, 3)

    if value == 1:
        return orange_waste()
    elif value == 2:
        return bottle_waste()
    else:
        return paper_waste()


def orange_waste():
    return WasteSprite(image=games.load_image('Orange.png'), type_name='orange')


def bottle_waste():
    return WasteSprite(image=games.load_image('bottle.jpg'), type_name='bottle')


def paper_waste():
    return WasteSprite(image=games.load_image('paper.jpg'), type_name='paper')


games.screen.add(bin_orange)
games.screen.add(bin_bottle)
games.screen.add(bin_paper)
games.screen.add(builder)
games.screen.add(builder)

games.screen.mainloop()
