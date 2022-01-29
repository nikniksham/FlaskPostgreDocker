import os
print("." + "\\".join(os.path.abspath("db/db_for_proj.sql").split("\\")[:-1]))