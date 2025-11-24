➜  brief-ci-cd-semantic-release-mkdocs git:(main) ✗ uv run ruff check      
F401 [*] `sys` imported but unused
  --> app/database.py:9:8
   |
 7 | from sqlmodel import create_engine, Session
 8 | import os
 9 | import sys
   |        ^^^
10 | from typing import Generator
   |
help: Remove unused import: `sys`

F401 [*] `typing.Generator` imported but unused
  --> app/database.py:10:20
   |
 8 | import os
 9 | import sys
10 | from typing import Generator
   |                    ^^^^^^^^^
11 |
12 | DATABASE_URL = os.getenv(
   |
help: Remove unused import: `typing.Generator`

F401 [*] `os` imported but unused
 --> app/main.py:2:8
  |
1 | from contextlib import asynccontextmanager
2 | import os
  |        ^^
3 | import sys
4 | from fastapi import FastAPI
  |
help: Remove unused import: `os`

F401 [*] `sys` imported but unused
 --> app/main.py:3:8
  |
1 | from contextlib import asynccontextmanager
2 | import os
3 | import sys
  |        ^^^
4 | from fastapi import FastAPI
5 | from sqlmodel import SQLModel
  |
help: Remove unused import: `sys`

F401 [*] `json` imported but unused
 --> app/main.py:6:8
  |
4 | from fastapi import FastAPI
5 | from sqlmodel import SQLModel
6 | import json
  |        ^^^^
7 | from typing import Dict, Any
8 | from app.database import engine
  |
help: Remove unused import: `json`

F401 [*] `typing.Dict` imported but unused
 --> app/main.py:7:20
  |
5 | from sqlmodel import SQLModel
6 | import json
7 | from typing import Dict, Any
  |                    ^^^^
8 | from app.database import engine
9 | from app.routes import items_router
  |
help: Remove unused import

F401 [*] `typing.Any` imported but unused
 --> app/main.py:7:26
  |
5 | from sqlmodel import SQLModel
6 | import json
7 | from typing import Dict, Any
  |                          ^^^
8 | from app.database import engine
9 | from app.routes import items_router
  |
help: Remove unused import

F401 [*] `typing.Optional` imported but unused
 --> app/models/item.py:2:20
  |
1 | from sqlmodel import Field, SQLModel
2 | from typing import Optional
  |                    ^^^^^^^^
3 |
4 | class Item(SQLModel, table=True):
  |
help: Remove unused import: `typing.Optional`

F401 [*] `typing.List` imported but unused
 --> app/routes/items.py:3:20
  |
1 | from fastapi import APIRouter, Depends, HTTPException, status
2 | from sqlmodel import Session
3 | from typing import List
  |                    ^^^^
4 | import datetime
  |
help: Remove unused import: `typing.List`

F401 [*] `datetime` imported but unused
 --> app/routes/items.py:4:8
  |
2 | from sqlmodel import Session
3 | from typing import List
4 | import datetime
  |        ^^^^^^^^
5 |
6 | from app.database import get_db
  |
help: Remove unused import: `datetime`

F401 [*] `typing.Optional` imported but unused
 --> app/schemas/item.py:2:20
  |
1 | from sqlmodel import Field, SQLModel
2 | from typing import Optional
  |                    ^^^^^^^^
3 |
4 | class ItemBase(SQLModel):
  |
help: Remove unused import: `typing.Optional`

Found 11 errors.
[*] 11 fixable with the `--fix` option.



concernant mypy, 