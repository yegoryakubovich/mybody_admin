#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from peewee import Model, PrimaryKeyField, MySQLDatabase, IntegerField, ForeignKeyField, CharField, BigIntegerField

from config import MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, SETTINGS_TEXT_404

db = MySQLDatabase(
    database=MYSQL_NAME,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    charset='utf8mb4',
    autoconnect=False,
)


class BaseModel(Model):
    class Meta:
        database = db


class Language(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)

    class Meta:
        db_table = 'languages'


class Account(BaseModel):
    id = PrimaryKeyField()
    adecty_account_id = IntegerField()
    language = ForeignKeyField(Language, to_field='id')

    def text_get(self, key):
        text = Text.get_or_none(Text.key == key)
        if not text:
            return SETTINGS_TEXT_404

        translate = Translate.get_or_none((Translate.text == text) & (Translate.language == self.language))
        if not translate:
            translate = Translate.get(Translate.text == text)

        return translate.value

    class Meta:
        db_table = 'accounts'


class Admin(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')

    class Meta:
        db_table = 'admins'


class Text(BaseModel):
    id = PrimaryKeyField()

    class Meta:
        db_table = 'items'


class Translate(BaseModel):
    id = PrimaryKeyField()
    language = ForeignKeyField(Language, backref='translates')
    text = ForeignKeyField(Text, backref='translates')
    value = CharField()

    class Meta:
        db_table = 'translates'


class Item(BaseModel):
    id = PrimaryKeyField()
    key = CharField()
    text = ForeignKeyField(Text, to_field='id')

    class Meta:
        db_table = 'items'


class Article(BaseModel):
    id = PrimaryKeyField()
    name = ForeignKeyField(Text, to_field='id')

    class Meta:
        db_table = 'articles'


class ArticleItem(BaseModel):
    id = PrimaryKeyField()
    article = ForeignKeyField(Article, to_field='id', backref='article_items')
    path = BigIntegerField()
    type = CharField()
    data = CharField()

    class Meta:
        db_table = 'articles_items'
