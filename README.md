Mon
===

- author: Ondrej Sika <ondrej@ondrejsika.com>
- license: MIT <https://ondrejsika.com/license/mit.txt>

Simple self hosted website monitor

Install
-------

```
git clone https://github.com/ondrejsika/mon.git
cd mon
cp conf--template.py conf.py
# vim conf.py
virtualenv .env
. .env/bin/activate
pip install -r requirements.txt
```

Run
---

```
./mon.py
```

