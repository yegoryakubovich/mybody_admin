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


from flask import Blueprint, request, redirect, json

from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputButton, Button, ButtonType, Form, InputText, Card, View, \
    ViewType
from peewee import DoesNotExist

from app.adecty_design.interface import interface
from app.blueprints.articles.arcicle.chapters import blueprint_chapters
from app.database.models import Article, Admin, ArticleItem, Account
from app.database import Text as TextDB
from app.decorators.admin_get import admin_get


blueprint_article = Blueprint(
    name='blueprint_article',
    import_name=__name__,
    url_prefix='/<int:article_id>/'
)

blueprint_article.register_blueprint(blueprint=blueprint_chapters)


@blueprint_article.route(rule='/update', endpoint='update', methods=['GET', 'POST'])
@admin_get()
def articles_update(admin: Admin, article_id: int):
    article = Article.get_or_none(Article.id == article_id)
    account = Account.get_by_id(admin.account_id)
    article_name = article.name.value_get(account)
    root_blocks = ArticleItem.select().where((ArticleItem.path == 0) & (ArticleItem.article == article))
    widgets = []
    widgets.append(
        Text(
            text=article_name,
            font=Font(size=50),
            margin=Margin(down=16)
        )
    )

    for block in root_blocks:
        if block.type == 'text':
            card_widgets = []

            block_data = json.loads(block.data)

            if 'text' in block_data:
                text_id = block_data['text']
                if text_id:
                    text = TextDB.get_or_none(TextDB.id == text_id)
                    if text:
                        value = text.value_get(account)
                        card_widgets.append(
                            Text(
                                text=value,
                                font=Font(size=14),
                                margin=Margin(down=8)
                            )
                        )

            card_widgets.extend([
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            url=f'/articles/{article_id}/{block.id}/text/edit'
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать раздел',
                            url=f'/articles/{article_id}/{block.id}',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            url=f'/articles/{article_id}/{block.id}/delete'
                        )
                    ]
                )
            ])

            widgets.append(
                Card(
                    widgets=card_widgets,
                    margin=Margin(down=16)
                )
            )

    for block in root_blocks:
        if block.type == 'chapter':
            block_widgets = []

            block_data = json.loads(block.data)

            if 'text' in block_data:
                text_id = block_data['text']
                if text_id:
                    text = TextDB.get_or_none(TextDB.id == text_id)
                    if text:
                        value = text.value_get(account)
                        block_widgets.append(
                            Text(
                                text=value,
                                font=Font(size=14),
                                margin=Margin(down=8)
                            )
                        )

            block_widgets.extend([
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            url=f'/articles/{article_id}/{block.id}/text/edit'
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать раздел',
                            url=f'/articles/{article_id}/{block.id}'
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            url=f'/articles/{article_id}/{block.id}/delete'
                        )
                    ]
                )
            ])

            widgets.append(
                Card(
                    widgets=block_widgets,
                    margin=Margin(down=16)
                )
            )

    add_block_button = Button(
        type=ButtonType.chip,
        text='Добавить раздел',
        url=f'/articles/{article_id}/block'
    )
    widgets.append(add_block_button)

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles'
    )

    return interface_html


@blueprint_article.route(rule='/block', endpoint='block', methods=['GET', 'POST'])
@admin_get(not_return=True)
def articles_block(article_id: int):
    widgets = [
        Card(
            widgets=[
                Button(
                    text='Обычный текст',
                    url=f'/articles/{article_id}/text/create',
                    margin=Margin(down=8)
                ),
                Button(
                    text='Раздел',
                    url=f'/articles/{article_id}/chapter/create',
                    margin=Margin(down=8)
                )
            ],
            margin=Margin(down=16)
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_article.route(rule='/text/create', endpoint='text_create', methods=['GET', 'POST'])
@admin_get(not_return=True)
def articles_text_add(article_id: int):
    if request.method == 'POST':
        text = request.form.get('name')

        new_text = TextDB()
        new_text.save()
        new_text.default_create(value=text)

        article_item = ArticleItem(
            article=article_id,
            path=0,
            type='text',
            data='{"text": ' + str(new_text.id) + '}'
        )

        article_item.save()

        return redirect(f'/articles/{article_id}/update')

    widgets = [
        Form(
            widgets=[
                Text(
                    text='Текст:',
                    font=Font(
                        size=14,
                        weight=700,
                    )
                ),
                InputText(id='name'),
                InputButton(text='Создать', margin=Margin(horizontal=8))
            ]
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_article.route(rule='/chapter/create', endpoint='text_add', methods=['GET', 'POST'])
@admin_get(not_return=True)
def articles_text_add(article_id: int):
    if request.method == 'POST':
        text = request.form.get('name')

        new_text = TextDB()
        new_text.save()
        new_text.default_create(value=text)

        article_item = ArticleItem(
            article=article_id,
            path=0,
            type='text',
            data='{"text": ' + str(new_text.id) + '}'
        )

        article_item.save()

        return redirect(f'/articles/{article_id}/update')

    widgets = [
        Form(
            widgets=[
                Text(
                    text='Название раздела:',
                    font=Font(
                        size=14,
                        weight=700,
                    )
                ),
                InputText(id='name'),
                InputButton(text='Создать', margin=Margin(horizontal=8))
            ]
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_article.route(rule='/delete', endpoint='delete', methods=['GET', 'POST'])
@admin_get(not_return=True)
def article_delete(article_id):
    try:
        article = Article.get_by_id(article_id)
    except DoesNotExist:
        return redirect('/articles')
    ArticleItem.delete().where(ArticleItem.article_id == article_id).execute()
    article.delete_instance()
    return redirect('/articles')
