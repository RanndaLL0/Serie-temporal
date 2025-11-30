import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import redis.exceptions

r = redis.Redis(
    host='redis-13200.crce216.sa-east-1-2.ec2.cloud.redislabs.com',
    port=13200,
    decode_responses=True,
    username="default",
    password="o3lq21mCTKPTi4BaMmbKzhBM8XKTCeZh",
)

user1 = {
    "name": "Paul John",
    "email": "paul.john@example.com",
    "age": 42,
    "city": "London"
}

user2 = {
    "name": "Eden Zamir",
    "email": "eden.zamir@example.com",
    "age": 29,
    "city": "Tel Aviv"
}

user3 = {
    "name": "Paul Zamir",
    "email": "paul.zamir@example.com",
    "age": 35,
    "city": "Tel Aviv"
}

try:
    r.ft("idx:users").dropindex(True)
except redis.exceptions.ResponseError:
    pass

r.delete("user:1", "user:2", "user:3")

schema = (
    TextField("$.name", as_name="name"),
    TagField("$.city", as_name="city"),
    NumericField("$.age", as_name="age")
)

indexCreated = r.ft("idx:users").create_index(
    schema,
    definition=IndexDefinition(
        prefix=["user:"], index_type=IndexType.JSON
    )
)

user1Set = r.json().set("user:1", Path.root_path(), user1)
user2Set = r.json().set("user:2", Path.root_path(), user2)
user3Set = r.json().set("user:3", Path.root_path(), user3)

findPaulResult = r.ft("idx:users").search(
    Query("Paul @age:[30 40]")
)

print(findPaulResult)
# >>> Result{1 total, docs: [Document {'id': 'user:3', ...

citiesResult = r.ft("idx:users").search(
    Query("Paul").return_field("$.city", as_field="city")
).docs

print(citiesResult)
# >>> [Document {'id': 'user:1', 'payload': None, ...

req = aggregations.AggregateRequest("*").group_by(
    '@city', reducers.count().alias('count')
)

aggResult = r.ft("idx:users").aggregate(req).rows
print(aggResult)
# >>> [['city', 'London', 'count', '1'], ['city', 'Tel Aviv', 'count', '2']]

try:
    r.ft("hash-idx:users").dropindex(True)
except redis.exceptions.ResponseError:
    pass

r.delete("huser:1", "huser:2", "huser:3")

hashSchema = (
    TextField("name"),
    TagField("city"),
    NumericField("age")
)

hashIndexCreated = r.ft("hash-idx:users").create_index(
    hashSchema,
    definition=IndexDefinition(
        prefix=["huser:"], index_type=IndexType.HASH
    )
)

huser1Set = r.hset("huser:1", mapping=user1)
huser2Set = r.hset("huser:2", mapping=user2)
huser3Set = r.hset("huser:3", mapping=user3)

findPaulHashResult = r.ft("hash-idx:users").search(
    Query("Paul @age:[30 40]")
)

print(findPaulHashResult)
# >>> Result{1 total, docs: [Document {'id': 'huser:3',
# >>>   'payload': None, 'name': 'Paul Zamir', ...

r.close()
