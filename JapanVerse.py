from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Tuple, TypeVar
from functools import reduce
import time

T = TypeVar("T")

def traced(fn: Callable[..., T]) -> Callable[..., T]:
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        duration = (time.perf_counter() - start) * 1000
        print(f"[TRACE] {fn.__name__} took {duration:.2f}ms")
        return result
    return wrapper

def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def normalize_str(value: str) -> str:
    return " ".join(value.strip().lower().split())

@dataclass
class Entity:
    id: int
    name: str
    tags: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        ensure(isinstance(self.id, int) and self.id >= 0, "Invalid id")
        ensure(isinstance(self.name, str) and self.name.strip(), "Invalid name")
        self.name = self.name.strip()
        self.tags = tuple(map(lambda t: normalize_str(str(t)), self.tags))

    @property
    def kind(self) -> str:
        return self.__class__.__name__

    def has_tag(self, tag: str) -> bool:
        return normalize_str(tag) in self.tags

@dataclass
class Media(Entity):
    year: int = 0
    rating: float = 0.0
    studio: str = ""

    def __post_init__(self):
        super().__post_init__()
        ensure(1900 <= self.year <= 2100, "Invalid year")
        ensure(0.0 <= self.rating <= 10.0, "Invalid rating")
        self.studio = self.studio.strip()

    def is_classic(self) -> bool:
        return self.year <= 2005 and self.rating >= 8.0

@dataclass
class Anime(Media):
    episodes: int = 0
    genre: str = ""

    def __post_init__(self):
        super().__post_init__()
        ensure(self.episodes >= 0, "Invalid episodes")
        self.genre = self.genre.strip()

    def binge_score(self) -> float:
        if self.episodes == 0:
            return self.rating
        return round((self.rating * 10) / (1 + self.episodes / 12), 2)

@dataclass
class Drama(Media):
    seasons: int = 1
    platform: str = ""

    def __post_init__(self):
        super().__post_init__()
        ensure(self.seasons >= 1, "Invalid seasons")
        self.platform = self.platform.strip()

@dataclass
class Tech(Entity):
    field: str = ""
    year: int = 0

    def __post_init__(self):
        super().__post_init__()
        ensure(1900 <= self.year <= 2100, "Invalid tech year")
        self.field = self.field.strip()

@dataclass
class Company(Tech):
    hq_city: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.hq_city = self.hq_city.strip()

@dataclass
class Gadget(Tech):
    maker: str = ""
    spec_score: int = 0

    def __post_init__(self):
        super().__post_init__()
        ensure(0 <= self.spec_score <= 100, "Invalid spec score")
        self.maker = self.maker.strip()

@dataclass
class Link(Entity):
    src_id: int = 0
    dst_id: int = 0
    rel: str = ""

    def __post_init__(self):
        super().__post_init__()
        ensure(self.src_id >= 0 and self.dst_id >= 0, "Invalid link ids")
        self.rel = normalize_str(self.rel)

class Index:
    def __init__(self, key_fn: Callable[[Entity], Any]):
        self.key_fn = key_fn
        self.map: Dict[Any, set[int]] = {}

    def add(self, row: Entity):
        key = self.key_fn(row)
        self.map.setdefault(key, set()).add(row.id)

    def remove(self, row: Entity):
        key = self.key_fn(row)
        if key in self.map:
            self.map[key].discard(row.id)
            if not self.map[key]:
                del self.map[key]

    def lookup(self, key: Any) -> set[int]:
        return set(self.map.get(key, set()))

class Table(Generic[T]):
    def __init__(self, name: str):
        self.name = name
        self.rows: Dict[int, T] = {}
        self.indices: Dict[str, Index] = {}
        self.history_log: List[str] = []

    def create_index(self, name: str, key_fn: Callable[[T], Any]):
        ensure(name not in self.indices, "Index exists")
        idx = Index(key_fn)
        for row in self.rows.values():
            idx.add(row)
        self.indices[name] = idx
        self.history_log.append(f"INDEX {self.name}.{name}")

    @traced
    def insert(self, row: T):
        ensure(row.id not in self.rows, "Duplicate id")
        self.rows[row.id] = row
        for idx in self.indices.values():
            idx.add(row)
        self.history_log.append(f"INSERT {self.name} {row.id}")

    @traced
    def delete(self, row_id: int):
        ensure(row_id in self.rows, "Row not found")
        row = self.rows[row_id]
        for idx in self.indices.values():
            idx.remove(row)
        del self.rows[row_id]
        self.history_log.append(f"DELETE {self.name} {row_id}")

    @traced
    def update(self, row_id: int, **changes):
        ensure(row_id in self.rows, "Row not found")
        row = self.rows[row_id]
        for idx in self.indices.values():
            idx.remove(row)
        for key, value in changes.items():
            setattr(row, key, value)
        row.__post_init__()
        for idx in self.indices.values():
            idx.add(row)
        self.history_log.append(f"UPDATE {self.name} {row_id}")

    def all(self) -> Iterator[T]:
        return iter(self.rows.values())

    def where(self, predicate: Callable[[T], bool]) -> Iterator[T]:
        return filter(predicate, self.rows.values())

    def by_index(self, index_name: str, key: Any) -> Iterator[T]:
        ensure(index_name in self.indices, "Index not found")
        ids = self.indices[index_name].lookup(key)
        return map(lambda i: self.rows[i], ids)

class JapanVerseDB:
    def __init__(self):
        self.media = Table("media")
        self.tech = Table("tech")
        self.links = Table("links")
        self.media.create_index("kind", lambda r: r.kind)
        self.media.create_index("studio", lambda r: normalize_str(r.studio))
        self.tech.create_index("field", lambda r: normalize_str(r.field))
        self.links.create_index("rel", lambda r: r.rel)

    def search(self, keyword: str):
        k = normalize_str(keyword)
        return list(filter(lambda e: k in normalize_str(e.name), list(self.media.all()) + list(self.tech.all())))

    def top_anime(self, n: int):
        animes = filter(lambda m: isinstance(m, Anime), self.media.all())
        scored = map(lambda a: (a.binge_score(), a), animes)
        return list(map(lambda x: x[1], sorted(scored, reverse=True)[:n]))

    def avg_rating_by_studio(self):
        groups: Dict[str, List[float]] = {}
        for m in self.media.all():
            groups.setdefault(normalize_str(m.studio), []).append(m.rating)
        return {k: round(reduce(lambda a, b: a + b, v) / len(v), 2) for k, v in groups.items()}

def seed(db: JapanVerseDB):
    db.media.insert(Anime(1, "Steins;Gate", ("time travel", "tokyo"), 2011, 9.0, "White Fox", 24, "Sci-Fi"))
    db.media.insert(Anime(2, "Vinland Saga", ("war", "growth"), 2019, 8.8, "WIT", 48, "Historical"))
    db.media.insert(Drama(3, "Midnight Diner", ("tokyo", "food"), 2009, 8.4, "MBS", 3, "Netflix"))
    db.tech.insert(Company(100, "Sony", ("hardware",), "electronics", 1946, "Tokyo"))
    db.tech.insert(Gadget(200, "Aibo", ("robot", "ai"), "robotics", 1999, "Sony", 85))

def print_entity(e: Entity):
    print(e)

def run():
    db = JapanVerseDB()
    seed(db)
    while True:
        print("\n1 Media\n2 Tech\n3 Search\n4 Top Anime\n5 Avg Rating\n0 Exit")
        c = input("Choose: ").strip()
        if c == "1":
            list(map(print_entity, db.media.all()))
        elif c == "2":
            list(map(print_entity, db.tech.all()))
        elif c == "3":
            k = input("Keyword: ")
            list(map(print_entity, db.search(k)))
        elif c == "4":
            print(db.top_anime(3))
        elif c == "5":
            print(db.avg_rating_by_studio())
        elif c == "0":
            break

if __name__ == "__main__":
    run()
