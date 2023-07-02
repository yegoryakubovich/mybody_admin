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


from flask import Blueprint, request, redirect
import json
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputButton, Button, ButtonType, Form, InputText, Card, View, ViewType
from app.adecty_design.interfaces import interface
from app.blueprints.articles.arcicle.chapters.chapter import blueprint_chapter
from app.database.models import Admin, ArticleItem, Account
from app.database import Text as TextDB
from app.decorators.admin_get import admin_get


blueprint_chapters = Blueprint(
    name='blueprint_chapters',
    import_name=__name__,
    url_prefix='/<int:block_id>/'
)

blueprint_chapters.register_blueprint(blueprint=blueprint_chapter)


@blueprint_chapters.route(rule='/', endpoint='block_update', methods=['GET', 'POST'])
@admin_get()
def block_update(admin: Admin, article_id: int, block_id: int):
    root_block = ArticleItem.get_or_none(ArticleItem.id == block_id)
    account = Account.get_by_id(admin.account_id)

    widgets = []

    related_blocks = ArticleItem.select().where(
        (ArticleItem.article == root_block.article) &
        (ArticleItem.path == root_block.id)
    )

    for related_block in related_blocks:
        if related_block and related_block.type in ['text', 'image', 'youtube']:
            block_data = json.loads(related_block.data)
            card_widgets = []

            if 'url' in block_data:
                url_id = block_data['url']
                if url_id:
                    url = TextDB.get_or_none(TextDB.id == url_id)
                    if url:
                        url_value = url.value_get(account)
                        card_widgets.append(
                            Text(
                                text=url_value,
                                font=Font(size=14),
                                margin=Margin(down=8)
                            )
                        )

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

            card_widgets.append(
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            url=f'/articles/{article_id}/{block_id}/{related_block.id}/edit'
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            url=f'/articles/{article_id}/{block_id}/{related_block.id}/deleted'
                        )
                    ]
                )
            )

            widgets.append(
                Card(
                    widgets=card_widgets,
                    margin=Margin(down=16)
                )
            )

    create_buttons = [
        Button(
            type=ButtonType.chip,
            text='Создать текст',
            url=f'/articles/{article_id}/{block_id}/text/create'
        ),
        Button(
            type=ButtonType.chip,
            text='Создать картинку',
            url=f'/articles/{article_id}/{block_id}/image/create'
        ),
        Button(
            type=ButtonType.chip,
            text='Создать видео',
            url=f'/articles/{article_id}/{block_id}/video/create'
        )
    ]

    widgets.append(
        View(
            type=ViewType.horizontal,
            widgets=create_buttons
        )
    )

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles'
    )

    return interface_html


@blueprint_chapters.route(rule='/text/edit', endpoint='text_edit', methods=['GET', 'POST'])
@admin_get()
def articles_text_edit(admin: Admin, article_id: int, block_id: int):
    root_block = ArticleItem.get_or_none(ArticleItem.id == block_id)
    account = Account.get_by_id(admin.account_id)

    widgets = []

    if request.method == 'POST':
        new_value = request.form.get('new_value')
        root_block_data = json.loads(root_block.data)
        if root_block_data:
            if 'text' in root_block_data:
                if new_value:
                    text_id = root_block_data['text']
                    if text_id:
                        text = TextDB.get_or_none(TextDB.id == text_id)
                        if text:
                            text.value_set(account, new_value)
                        else:
                            new_text = TextDB()
                            new_text.save()
                            new_text.default_create(value=new_value)
                            root_block_data['text'] = new_text.id

        return redirect(f'/articles/{article_id}/update')

    if root_block:
        data = json.loads(root_block.data)
    else:
        data = {}

    text = ''

    if 'text' in data:
        text_id = data['text']
        if text_id:
            text_db = TextDB.get_or_none(TextDB.id == text_id)
            if text_db:
                text = text_db.value_get(account)

    widgets.append(
        Form(
            widgets=[
                Text(
                    text='Текст',
                    font=Font(size=14, weight=700),
                ),
                InputText(id='new_value', value=text),
                InputButton(text='Сохранить', margin=Margin(top=8)),
            ],
        )
    )

    interface_html = interface.html_get(widgets=widgets, active='articles')

    return interface_html


@blueprint_chapters.route(rule='/unit', endpoint='delete_block', methods=['GET', 'POST'])
@admin_get(not_return=True)
def delete_block(article_id: int, block_id: int):
    chapter = ArticleItem.get_or_none(ArticleItem.id == block_id)

    if chapter:
        chapter.delete_instance()

    return redirect(f'/articles/{article_id}/update')


@blueprint_chapters.route(rule='/image/create', endpoint='chapter_create_image', methods=['GET', 'POST'])
@admin_get(not_return=True)
def chapter_create_image(block_id: int, article_id: int):
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        value_text = request.form.get('value_text')

        new_url_text = TextDB(value=image_url)
        new_url_text.save()
        new_url_text.default_create(value=image_url)

        new_text_text = TextDB(value=value_text)
        new_text_text.save()
        new_text_text.default_create(value=value_text)

        chapter = ArticleItem.create(
            article=article_id,
            path=block_id,
            type='image',
            data='{"url": ' + str(new_url_text.id) + ', "text": ' + str(new_text_text.id) + '}'
        )

        chapter.save()

        return redirect(f'/articles/{article_id}/{block_id}')

    widgets = [
        Text(
            text='Создание картинки',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Текст',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='value_text'),
                Text(
                    text='URL',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='image_url'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_chapters.route(rule='/text/create', endpoint='chapter_create_text', methods=['GET', 'POST'])
@admin_get(not_return=True)
def chapter_create_text(block_id: int, article_id: int):
    if request.method == 'POST':
        text = request.form.get('text')

        new_text = TextDB()
        new_text.save()
        new_text.default_create(value=text)

        chapter = ArticleItem.create(
            article=article_id,
            path=block_id,
            type='text',
            data='{"text": ' + str(new_text.id) + '}'
        )

        chapter.save()

        return redirect(f'/articles/{article_id}/{block_id}')

    widgets = [
        Text(
            text='Создание текста',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Текст',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='text'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html


@blueprint_chapters.route(rule='/video/create', endpoint='chapter_create_video', methods=['GET', 'POST'])
@admin_get(not_return=True)
def chapter_create_video(block_id: int, article_id: int):
    if request.method == 'POST':
        video_url = request.form.get('video_url')

        new_text = TextDB()
        new_text.save()
        new_text.default_create(value=video_url)

        chapter = ArticleItem.create(
            article=article_id,
            path=block_id,
            type='youtube',
            data='{"url": ' + str(new_text.id) + '}'
        )

        chapter.save()

        return redirect(f'/articles/{article_id}/{block_id}')

    widgets = [
        Text(
            text='Создание видео',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Ссылка на видео',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='video_url'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html
