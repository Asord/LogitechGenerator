from json import loads
from tkinter import *

class jsonWindow(Tk):
    def __init__(self, file):
        Tk.__init__(self)

        self.__file = file
        self._config = {}
        self._binds = {}

    def generateGUI(self):
        data = self._getJsonConfig()

        if "title" in data:
            self.title(data["title"])
        if "geometry" in data:
            self.geometry(data["geometry"])
        if "resizable" in data:
            self.resizable(**data["resizable"])
        if "grid_rowconfigure" in data:
            _v = data["grid_rowconfigure"].pop("v")
            self.grid_rowconfigure(_v, **data["grid_rowconfigure"])
        if "grid_columnconfigure" in data:
            _v = data["grid_columnconfigure"].pop("v")
            self.grid_columnconfigure(_v, **data["grid_columnconfigure"])

        _counter = 0
        for e in data["elements"]:
            _name  = e["name"]
            _type  = e["type"]
            _param = e["param"] if "param" in e else {}
            _grid  = e["grid"] if "grid" in e else {}

            _master = self

            if "master" in _param:
                _master = _param.pop("master")

                if _master in self._config:
                    _master = self._config[_master]
                else:
                    print("Config initialization order mismatch")
                    print("master %s isn't generated (yet) [element %d]" % (_master, _counter))
                    break

            if _type == "Frame":
                self._config[_name] = Frame(_master, **_param)

            elif _type == "Label":
                self._config[_name] = Label(_master, **_param)

            elif _type == "Spinbox":
                self._config[_name] = Spinbox(_master, **_param)

            elif _type == "Canvas":
                self._config[_name] = Canvas(_master, **_param)

            elif _type == "Button":
                self.__resolve("command", _param, self._binds, "Button bind", _counter)
                self._config[_name] = Button(_master, **_param)

            elif _type == "Entry":
                self.__resolve("textvariable", _param, self._config, "TextVariable", _counter)
                self._config[_name] = Entry(_master, **_param)

            elif _type == "StringVar":
                self._config[_name] = StringVar()
                self._config[_name].set(_param.pop("v"))
                continue

            elif _type == "Menubar":
                this = self._config[_name] = Menu(self)

                for _,sub in _param.items():
                    _sName = sub["name"]
                    _sType = sub["type"]
                    _sParam = sub["param"]
                    _sContent = sub["content"]

                    if _sType == "MenuCascade":
                        sub = self._config[_sName] = Menu(this, tearoff=_sParam["tearoff"])
                        this.add_cascade(label=_sParam["label"], menu=sub)

                        for c in _sContent:

                            if c["type"] == "MenuCommand":
                                sub.add_command(label=c["label"], command=self._binds[c["command"]])

                self.config(menu=this)
                continue


            self._config[_name].grid(**_grid)

            _counter += 1

    def _getJsonConfig(self):
        try:
            with open(self.__file, "r") as fs:
                content = fs.read()
                return loads(content)
        except IOError:
            print("Json config file can't be found or readed...")
            return {}

    @staticmethod
    def __resolve(e, p, l, t="Object", c=0):
        if e in p:
            _tmp = p[e]
            if _tmp in l:
                p[e] = l[_tmp]
            else:
                p.pop(e)
                print("%s %s don't exist yet (element %d)" % (t, e, c))
