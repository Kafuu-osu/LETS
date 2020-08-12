## LeTs

SpECiAL THaNKs To [ReALisTIKosU](https://ussr.pl/) aND [AInU](https://ainu.pw/)

## 需要

python3.8


#### 初始化子模块
```
git submodule init
git submodule update
cd secret
git submodule init
git submodule update
cd ..
```

#### 安装依赖
```
pip38 install -r requirements.txt
```


#### 编译
```
python38 setup.py build_ext --inplace
```

#### 运行
```
python38 lets.py
```

#### 编辑配置
```
vim config.ini
```


#### 编译pp计算库

linux
```
cd ./pp/oppai-ng/ && chmod +x ./build && ./build && cd ./../../
cd ./pp/oppai-rx/ && chmod +x ./build && ./build && cd ./../../
cd ./pp/oppai-ap/ && chmod +x ./build && ./build && cd ./../../
```

windows
```
./build_oppai.ps1
```

#### 配置common/config.json

```
cd common
cp default_config.json config.json
vim config.json
```


## tomejerry.py


```
usage: tomejerry.py [-h]
                    [-r | -z | -i ID | -m MODS | -g GAMEMODE | -u USERID | -b BEATMAPID | -fhd]
                    [-w WORKERS] [-cs CHUNKSIZE] [-v]

pp recalc tool for ripple, new version.

optional arguments:
  -h, --help            show this help message and exit
  -r, --recalc          calculates pp for all high scores
  -z, --zero            calculates pp for 0 pp high scores
  -i ID, --id ID        calculates pp for the score with this score_id
  -m MODS, --mods MODS  calculates pp for high scores with these mods (flags)
  -g GAMEMODE, --gamemode GAMEMODE
                        calculates pp for scores played on this game mode
                        (std:0, taiko:1, ctb:2, mania:3)
  -u USERID, --userid USERID
                        calculates pp for high scores set by a specific user
                        (user_id)
  -b BEATMAPID, --beatmapid BEATMAPID
                        calculates pp for high scores played on a specific
                        beatmap (beatmap_id)
  -fhd, --fixstdhd      calculates pp for std hd high scores (14/05/2018 pp
                        algorithm changes)
  -w WORKERS, --workers WORKERS
                        number of workers. 16 by default. Max 32
  -cs CHUNKSIZE, --chunksize CHUNKSIZE
                        score chunks size
  -v, --verbose         verbose/debug mode
```

## License
This project is licensed under the GNU AGPL 3 License.  
See the "LICENSE" file for more information.  
