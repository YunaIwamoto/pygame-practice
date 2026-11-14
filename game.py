from encodings.punycode import T
from pse2pgzrun import * # type: ignore
import pygame  # type: ignore

# スクリーンサイズ
WIDTH = 800  # 横幅
HEIGHT = 600  # 縦幅
TITLE = 'RUNGAME'  # タイトル
#重力
GRAVITY = 0.8
#ジャンプ
JUMP = -16
# モード
PREPLAY = 0
INPLAY = 1
POSTPLAY = 2

# プレイヤークラス（Actorクラスを継承）
class Player(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.status = {
            "vx": 0, "vy": 0, "speed": 5,
            "jumping": False, "goal": False
        }

    def reset_image(self):
        self.image = 'character_idle'

    def update_physics(self,blocks,jump_sound):
        # ゴール後は動かない
        if self.status["goal"]:
            return 
    
        if self.right > WIDTH:
            self.right = WIDTH
        elif self.left < 0:
            self.left = 0
        
        self.status["vx"] = 0
        if keyboard.right:
            self.status["vx"] = self.status["speed"]
        if keyboard.left: 
            self.status["vx"] = -self.status["speed"]

        if keyboard.space and not self.status["jumping"]:
            self.status["vy"] = JUMP
            self.status["jumping"] = True
            self.y -= 2
            jump_sound.play()
            self.image = 'character_jump1'
            clock.schedule_unique(self.reset_image, 0.5)
        #重力
        self.status["vy"] += GRAVITY
        self.y += self.status["vy"]

        

        self.status["jumping"] = True
        
        for b in blocks:
            if self.colliderect(b):
                # print("player",self.bottom)
                # print("b.top",b.top)
                # print("b.bottom:",b.bottom)
                if self.status["vy"] > 0 and self.bottom >= b.top and self.bottom <= b.bottom:
                    self.bottom = b.top
                    self.status["vy"] = 0
                    self.status["jumping"] = False
                
                 

#敵クラス(Actorを継承)
class Enemy(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.status = {
            "vx": -2, "vy": 0
        }

    def update(self, blocks, lose_sound, hurt_sound):
        self.x += self.status["vx"]
        for b in blocks:
            if self.colliderect(b):
                if self.status["vy"] > 0:
                    self.bottom = b.top


# ブロッククラス（Actorを継承）
class Block(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)

class Coin(Actor):
    def __init__(self, image, pos):
        super().__init__(image,pos)        


class Game:
    def __init__(self):
        self.start()
        # 音
        self.tone_win = tone.create('A5', 1.0)
        self.tone_lose = sounds.disappear
        self.tone_jump = sounds.jump
        self.tone_hurt = sounds.hurt
        self.tone_coin = sounds.coin
        #スクリーン
        self.screen = pygame.display.set_mode((800, 600))
        # 背景画像の読み込み
        self.bg_image = pygame.image.load("background_fade_desert.png")
        self.scroll_total = 0
        # 画面サイズに合わせる
        #self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        #プレイヤー
        self.player = Player('character_idle',(100, 450))
        #敵
        self.enemies =[]
        self.enemies.append(Enemy('slime_normal_walk_a', (500, 520)))
        self.enemies.append(Enemy('slime_normal_walk_a', (600, 520)))
        self.enemies.append(Enemy('bee_a',( 2000, 300)))
        self.enemies.append(Enemy('bee_a',( 2500, 300)))
        self.enemies.append(Enemy('bee_a',( 2300, 500)))
        #コイン
        self.coin_count = 0
        self.coins = []
        for x in range(800, 1100, 100):
            for y in range(150, 300, 100):
                self.coins.append(Coin('coin',(x, y)))
        
        for x in range(800, 1100, 100):
            for y in range(400, 550, 100):
                self.coins.append(Coin('coin',(x, y)))
        
        for x in range(1500, 1800, 100):
            for y in range(400, 550, 100):
                self.coins.append(Coin('coin',(x, y)))

        for x in range(1500, 1800, 100):
            for y in range(150, 400, 100):
                self.coins.append(Coin('coin',(x, y)))

        for x in range(1300, 1500, 100):
            for y in range(150, 400, 100):
                self.coins.append(Coin('coin',(x, y)))
        #ゴール
        self.goal = Actor('flag', (2000, 510)) 
        #ブロック
        self.blocks = []
        # 地面
        for x in range(0, 800, 60):
            self.blocks.append(Block('terrain_grass_block_top', (x, 570)))
        for x in range(1000, 1200, 60):
            self.blocks.append(Block('terrain_grass_block_top', (x, 570)))
        for x in range(1450, 2300, 60):
            self.blocks.append(Block('terrain_grass_block_top', (x, 570)))
        
        # 途中の足場
        for x in range(400, 700, 60):
            self.blocks.append(Block('terrain_grass_block_top', (x, 400)))

        for x in range(600, 800, 60):
            self.blocks.append(Block('terrain_grass_block_top', (x, 300)))
        
        for x in range(1000, 1200, 60):
            self.blocks.append(Block('terrain_grass_block_top', (x, 300)))
         
        
    def start(self):
        self.mode = PREPLAY
        self.humanwin = False  
    def update(self):
        if self.mode == PREPLAY:
            if keyboard.s:
                self.mode = INPLAY
            return
        
        if self.mode == INPLAY:
            self.player.update_physics(self.blocks,self.tone_jump)
            SCROLL_LIMIT = 1750
            #横スクロール
            if self.player.status["vx"] > 0 and self.player.x > 250 and self.scroll_total < SCROLL_LIMIT:
                scroll_speed = self.player.status["vx"]
                self.scroll_total += scroll_speed
                #すべての物体を左にズラす
                for b in self.blocks:
                    b.x -= scroll_speed
                self.goal.x -= scroll_speed
                for e in self.enemies:
                    e.x -= scroll_speed
                for c in self.coins:
                    c.x -= scroll_speed
            else:
                # 画面左端や中央より左なら普通に歩く
                self.player.x += self.player.status["vx"]

            for e in self.enemies:
                e.update(self.blocks, self.tone_lose, self.tone_hurt)
                if self.player.colliderect(e):   
                    if self.player.status["vy"] > 0 and self.player.bottom < e.y:
                        #倒したら消える
                        self.enemies.remove(e)
                        # 倒した反動で少し跳ねる
                        self.player.status["vy"] = -10 
                        self.tone_hurt.play() # type: ignore
                        self.coin_count += 2
                    else:
                        self.player.image = 'character_hit1'
                        # 横から当たった場合はゲームオーバー
                        self.player.status["goal"] = False
                        self.mode = POSTPLAY 
                        self.tone_lose.play() # type: ignore
                                
            for c in self.coins:
                if self.player.colliderect(c):
                    self.coin_count += 1    
                    self.coins.remove(c)    # コインを消す
                    self.tone_coin.play() # type: ignore

            if self.player.colliderect(self.goal):
                self.player.status["goal"] = True
                self.mode = POSTPLAY
                self.tone_win.play()
                self.player.image = 'character_jump1'

            if self.player.y > HEIGHT:
                self.player.status["goal"] = False
                self.mode = POSTPLAY  
                self.tone_lose.play() # type: ignore   

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        for b in self.blocks: #ブロックを描画
            b.draw()
        for e in self.enemies: # 敵を描画
            e.draw()
        for c in self.coins: #コインを描写
            c.draw()
        self.goal.draw()
        self.player.draw()
        screen.draw.text(
            f"COINS: {self.coin_count}", 
            topleft=(20, 20), 
            fontsize=50, 
            color='yellow',
            shadow=(1, 1),
            scolor='orange'
        )
        if self.mode == PREPLAY:
            screen.draw.text(
                'Start s key',
                center=(275, 300), fontsize=70, color='magenta')
        elif self.mode == POSTPLAY:
            if self.player.status["goal"]:
                screen.draw.text(
                    "GOAL!",
                    center=(275, 300), fontsize=100, color='green')
            else:
                screen.draw.text(
                    'Game Over...',
                    center=(275, 300), fontsize=100, color='red')

game = Game()


def draw():
    game.draw()


def update():
    game.update()


pgzrun.go()