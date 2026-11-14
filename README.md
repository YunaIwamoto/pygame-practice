# pygame-practice
大学でPython初学者向けの講座にて、文法理解・開発方法の学習が目的で行われた課題である。  
オープンソースライブラリであるPygame Zero(Pygame)を使用したゲームの作成課題<br>

# 遊び方
* 内容
　敵を倒したり避けながらコインを集めゴールを目指す。
* ルール
　敵は上から踏んで倒すことが出来る。  
  一度右に進むと表示画面が左には戻らない。  
　コインに触れるとゲット  
　また敵を倒すと＋２コインゲット。  
　しかし敵に当たったり、落ちてしまうとGame Over...  

* 操作方法
　ゲーム前  
　　"s"キーをクリックしてゲーム開始  
　ゲーム中  
　　矢印キー　　：→で右に移動  
　　　　　　　　：←で左に移動  
　　スペースキー：ジャンプ  

# 工夫点
* 辞書の機能を使って、プレイヤーの動きがどうなっているのかを判定できるようにした点。  
* Actorクラスのcolliderectを使い、プレイヤーのbottomがブロックのtopに重なったときにcolliderectが反応するようにした点。  
* clock.schedule_uniqueを使うことで、何回も同じ動作があった場合重複して動作が止まらないようにした点。  
* コインの獲得数を黄色で見にくくならないようにshadowを使った点。  
* スクロールをプレイヤーがいる位置があまり画面のギリギリにならないようにし、初心者でもゴールしやすくした点。  
　
# 参考にしたサイト
　　--敵にプレイヤーが当たったときの判定を加えるため、colliderect関数を使う方法を参考にした。参考にしたサイトは下記に示す。  
https://zenn.dev/kwaka1208/books/pygame-programming/viewer/07_hit  
　　--また、ゲームの背景を画像に変更したかったため以下のサイトを参考にした。  
https://zenn.dev/kwaka1208/books/pygame-programming/viewer/07_hit  
　  --跳ねた時の画像を一瞬時変更するためにschedule_uniqueの使い方をサイトで見つけ、使用した。  
https://pygame-zero.readthedocs.io/ja/latest/builtins.html  


# 画像や音のデータの入手方法・作成方法
　KenneyのNew Platformer Packを主に使用。すべての画像の余白をキャラクターなどの大きさに合わせるためにトリミングをしている。  
* コイン　→　coin_gold.png をcoin.pngに名前を変更し使用。  
* プレイヤー　→　character_beige_idle.pngをcharacter_idleに変更し使用。ジャンプしている画像はcharacter_beige_jump.pngをcharacter_jump1.pngに変更し使用。  
* 敵　→　ハチはbee_a.png、スライム？はslime_normal_walk_a.pngを使用。  
* 足場　→　terrain_grass_block_top.pngを使用。  
* 背景　→　background_fade_desert.pngを使用。  
* ゴール　→flag_green_a.pngを使用。   

* 効果音　→　sfx_coin.oggをcoin.oggに変更.  
            sfx_disappear.oggをdisappear.oggに変更.   
            sfx_hurt.oggをhurt.oggに変更.   
            sfx_jump.oggをjump.oggに変更.   
* https://kenney.nl/assets/new-platformer-pack  