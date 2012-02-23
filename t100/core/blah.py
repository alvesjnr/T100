import pickle
import base_components

qq = base_components.Queue()
import StringIO
io = StringIO.StringIO()
pickle.dump(qq,io)
