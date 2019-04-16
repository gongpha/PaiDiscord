from abc import ABC, abstractmethod
import os
from importlib import import_module

class ProcImg(ABC) :
	local_desc = None
	command_name = None

	@property
	def name(self) :
		return self.__class__.__name__.lower()
	@abstractmethod
	def generate(self, users, members, avatars, date, kwargs) :
		raise NotImplementedError(
			f"none of generate : {self.name}"
)

def get_all_proc(dir) :
	proclist = []
	for e in os.listdir(dir) :
		if not e.startswith("imgproc_") and not e.endswith(".py") :
			continue
		m = import_module('proc.imggen.{}'.format(e.replace(".py","")))
		classlist = []
		if isinstance(m.classname, tuple) :
			for cs in m.classname :
				classlist.append(getattr(m, cs))
		else :
			classlist = getattr(m, m.classname)
		proclist.append((
			classlist,
			m.name,
			m.author,
			m.desc
		))
		print(f"Loaded ProcImg {m.classname}")
	return proclist
