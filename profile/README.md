# Profiling

## To Create

```sh
python3 -m cProfile -o profile/parscribe.pstats train.py config/profile.ast
```

## To Visualise

```sh
sudo pip3 install snakeviz
snakeviz profile/parscribe.pstats
```

## To generate SVG

```sh
#sudo apt-get install gprof2dot
#sudo pip3 install gprof2dot
gprof2dot -f pstats parscribe.pstats | dot -Tsvg -o parscribe.svg
```
